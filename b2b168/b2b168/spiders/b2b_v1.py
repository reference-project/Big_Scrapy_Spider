# -*- coding: utf-8 -*-
import scrapy
import re
import jieba.analyse
from hashlib import md5
from b2b168.items import B2B168Item
from scrapy.cmdline import execute



class B2bSpider(scrapy.Spider):
    name = 'b2b'
    allowed_domains = ['*']
    start_urls = ['https://www.b2b168.com/page-company.html']

    custom_settings = {
        # 'DOWNLOAD_DELAY': 270,  # 下载延迟 270秒
        # 'LOG_LEVEL': 'DEBUG',  # 打印日志等级
        # 下面两个设置 关闭SSL证书验证
        "DOWNLOAD_HANDLERS_BASE": {
            'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
            'http': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
            'https': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
            's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler',
        },
        # "DOWNLOAD_HANDLERS": {
        #     'https': 'b2b168.custom.downloader.handler.https.HttpsDownloaderIgnoreCNError',
        # },
    }

    def parse(self, response):
        li_list = response.xpath("//div[@class='map']//ul[@class='c-hangye']//li//a")
        for li in li_list:
            kind_href = li.xpath("./@href").extract_first()
            kind_name = li.xpath("./@title").extract_first()
            if kind_href:
                # print(kind_name,kind_href)
                kind_href = "https://www.b2b168.com" + kind_href
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_kind_list,
                    dont_filter=True
                )

    def parse_kind_list(self, response):
        dd_list = response.xpath("//div[@class='mach_list clearfix']//dl//dd//a")
        for dd in dd_list:
            s_kind_href = dd.xpath("./@href").extract_first()
            s_kind_name = dd.xpath("./@title").extract_first()
            if s_kind_href:
                s_kind_href = "https://www.b2b168.com" + s_kind_href
                yield scrapy.Request(
                    url=s_kind_href,
                    callback=self.parse_company_list,
                    dont_filter=True
                )

    def parse_company_list(self, response):
        li_list = response.xpath("//div[@class='cations']//ul[@class='list']//li")
        for li in li_list:
            company_href = li.xpath(".//div[@class='biaoti']/a/@href").extract_first()
            company_name = li.xpath(".//div[@class='biaoti']/a/@title").extract_first()
            linkman = li.xpath(".//div[@class='n_r']//p//span[@class='names']/text()").extract_first()
            kinds = li.xpath(".//div[@class='n_r']//p[@class='gs_n']/text()").extract_first()
            if kinds:
                kinds = re.sub(r'\s|\r|\t|\n','',kinds).replace(',', '|').replace(';','|').replace('、', '|').replace('，', '|')
            else:
                kinds = ''
            if company_href and "http:" in company_href:
                company_href = company_href
            else:
                company_href = "https:" + company_href
            yield scrapy.Request(
                url=company_href,
                callback=self.parse_company_contact,
                meta={
                    "url_info": company_href,
                    "kinds_info": kinds,
                },
                dont_filter=True
            )
        next_page_url = response.xpath("//div[@class='pages']//a[contains(text(),'下页')]/@href").extract_first()
        if next_page_url:
            next_page_url = "https://www.b2b168.com" + next_page_url
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_company_list,
                dont_filter=True
            )

    def parse_company_contact(self, response):
        kinds = response.meta.get("kinds_info")
        company_href = response.meta.get("url_info")
        if company_href and "www" in company_href:
            contact_href = company_href + "#lxfs"
        else:
            contact_href = company_href + "contact.aspx"
        if contact_href:
            yield scrapy.Request(
                url=contact_href,
                callback=self.parse_company_detail,
                meta={"kinds_info1": kinds},
                dont_filter=True
            )

    def parse_company_detail(self, response):
        # print(response.text)
        pattern = re.compile(r'公司名称：<a class="mBlue" href=".*?">(.*?)</a><br />',re.S)
        pattern1 = re.compile(r'<p class="com-pro"><span>主营：</span>(.*?)</p>',re.S)
        pattern2 = re.compile(r'联 系 人： <a class=b2>(.*?)</a><br />', re.S)
        pattern3 = re.compile(r'电　　话： (.*?)<br />', re.S)
        pattern4 = re.compile(r'传　　真： (.*?)<br />', re.S)
        pattern5 = re.compile(r'移动电话： (.*?)<br />', re.S)
        pattern6 = re.compile(r'<p>地址：(.*?)</p>', re.S)
        # 湖北省</a> 老河口市赞南村5组花园路西段
        pattern7 = re.compile(r'<dt>公司地址：</dt><dd><a href=".*?" title=".*?">(.*?)</dd>', re.S)
        pattern8 = re.compile(r'<dt>固定电话：</dt><dd>(.*?)</dd>', re.S)
        # <dt>联系人：</dt><dd>李文焕先生（）</dd>
        pattern9 = re.compile(r'<dt>联系人：</dt><dd>(.*?)</dd>', re.S)
        pattern10 = re.compile(r'<dt>移动电话：</dt><dd>(.*?)</dd>', re.S)
        pattern11 = re.compile(r'<dt>传真号码：</dt><dd>(.*?)</dd>', re.S)
        pattern12 = re.compile(r'"divMap","(.*?)",', re.S)
        pattern13 = re.compile(r'Messager： qq:(.*?)<br />')
        html_text = response.text
        if html_text:
            try:
                item = B2B168Item()
                item["company_Name"] = "".join(re.findall(pattern,html_text))
                item["kind"] = "".join(re.findall(pattern1,html_text)).replace(',','|').replace('，','|')
                item["linkman"] = "".join(re.findall(pattern2, html_text)).split(' ')[0].replace(' ','') if re.findall(pattern2, html_text) else ''
                item["telephone"] = "".join(re.findall(pattern3,html_text)).replace(' ','')
                item["contact_Fax"] = "".join(re.findall(pattern4,html_text)).replace(' ','')
                item["contact_QQ"] = "".join(re.findall(pattern13,html_text)).replace(' ','') if re.findall(pattern13,html_text) else ''
                item["phone"] = "".join(re.findall(pattern5,html_text)).replace(' ','')
                item["company_address"] = "".join(re.findall(pattern6, html_text)).replace(' ', '')
                item["Source"] = response.url
                if item["company_Name"]:
                    item["company_Name"] = item["company_Name"]
                else:
                    try:
                        item["company_Name"] = "".join(re.findall(pattern12, html_text))
                    except:
                        pass
                item["company_id"] = md5(item["company_Name"].encode()).hexdigest()
                if item["kind"]:
                    item["kind"] = re.sub(r'\s|\t|\r|\n|暂未提供|未填写|等', '', item["kind"]).replace(',', '|').replace(';','|').replace('、', '|')
                    item["kind"] = self.rinse_keywords(self.replace_ss(item["kind"]))
                else:
                    item["kind"] = response.meta.get("kinds_info1")
                if item["linkman"]:
                    item["linkman"] = self.search_linkman(item["linkman"])
                else:
                    try:
                        item["linkman"] = "".join(re.findall(pattern9,html_text)) if re.findall(pattern9,html_text) else ''
                        if item["linkman"] and "（" in item["linkman"]:
                            try:
                                item["linkman"] = item["linkman"].split('（')[0]
                            except:
                                item["linkman"] = ''
                        else:
                            item["linkman"] = item["linkman"]
                    except:
                        item["linkman"] = ''
                item["linkman"] = self.search_linkman(item["linkman"])
                if item["phone"]:
                    item["phone"] = self.search_phone_num(item["phone"])
                else:
                    try:
                        item["phone"] = "".join(re.findall(pattern10, html_text))
                    except:
                        item["phone"] = ''
                if item["telephone"]:
                    item["telephone"] = self.search_telephone_num(item["telephone"])
                else:
                    try:
                        item["telephone"] = "".join(re.findall(pattern8, html_text))
                    except:
                        item["telephone"] = ''

                if item["contact_Fax"]:
                    item["contact_Fax"] = self.search_contact_Fax(item["contact_Fax"])
                else:
                    try:
                        item["contact_Fax"] = "".join(re.findall(pattern11, html_text))
                    except:
                        item["contact_Fax"] = ''

                if item["company_address"]:
                    item["company_address"] = self.search_address(item["company_address"])
                else:
                    try:
                        item["company_address"] = response.xpath("//ul[contains(text(),'地址：')]/text()").extract_first()
                        if item["company_address"]:
                            item["company_address"] = self.search_address(item["company_address"])
                    except:
                        item["company_address"] = ''
                yield item
            except Exception as e:
                print(e)
                pass

    # 处理行业关键字
    def rinse_keywords(self, value):
        result_list = []
        for i in value.split('|'):
            result_list.append(
                ''.join(jieba.analyse.extract_tags(i, topK=5, withWeight=False,
                                                   allowPOS=('n', 'nz', 'v', 'vd', 'vn', 'l', 'a', 'd'))))
        result = '|'.join(set([i for i in result_list if i]))
        if result:
            return result
        else:
            return ''

    # replace 方法
    def replace_ss(self, text, args=''):
        if text:
            args = list(args) + ['\r', '\n', ' ', '\t', '\xa0', '\u3000']
            for i in args:
                text = text.replace(i, '')
            return text
        return ''

    # 清洗手机
    def search_phone_num(self, text):
        if text:
            try:
                pattern = re.compile(r'^1[35678]\d{9}$', re.S)
                text = re.sub(r'\s|\r|\t|\n|保密|移动电话：|电话：|未填写', '', text).strip()
                # text = re.search(r'1\d{10}',text).group(0)
                text = "".join(re.findall(pattern, text))
                return text
            except:
                return ''
        else:
            return ''

    # 清洗电话号码
    def search_telephone_num(self, text):
        if text:
            try:
                pattern = re.compile(r'\(?0\d{2,3}[)-]?\d{7,8}', re.S)
                text = re.sub(r'\s|\r|\t|\n|公司电话：|：|暂未提供|未填写', '', text).strip()
                text = "".join(re.findall(pattern, text))
                return text
            except:
                return ''
        else:
            return ''

    # 清洗传真号码
    def search_contact_Fax(self, text):
        if text:
            try:
                pattern = re.compile(r'\(?0\d{2,3}[)-]?\d{7,8}', re.S)
                # '公司联系人：胡'
                text = re.sub(r'\s|\r|\t|\n|公司传真：|：|暂未提供|未填写', '', text).strip()
                text = "".join(re.findall(pattern, text))
                return text
            except:
                return ''
        else:
            return ''

    # 清洗url
    def search_url(self, text):
        if text:
            try:
                pattern = re.compile(
                    r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|"
                    r"([a-zA-Z]+.\w+\.+[a-zA-Z0-9\/_]+)", re.S)
                text = "".join(re.findall(pattern, text))
                return text
            except:
                return ''

        else:
            return ''

    # 清洗email
    def search_email(self, text):
        if text:
            try:
                pattern = re.compile(r"[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+", re.S)
                text = re.sub(r'\s|\r|\t|\n|邮箱：|：|暂未提供', '', text).strip()
                text = "".join(re.findall(pattern, text))
                return text
            except:
                return ''
        else:
            return ""

    # 清洗QQ
    def search_QQ(self, text):
        if text:
            try:
                pattern = re.compile(r"([1-9]\d{4,10})@qq.com|([1-9]\d{4,10})", re.S)
                text = re.sub(r'\s|\r|\t|\n|QQ：|：|暂未提供|未填写', '', text).strip()
                text = "".join(re.findall(pattern, text))
                return text
            except:
                return ''
        else:
            return ''

    # 清洗联系人
    def search_linkman(self, text):
        if text:
            if len(text) >3:
                # text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写', '', text)[:3]
                # text = re.sub(r'\s|\r|\n|\t|先生|女士|小姐|联系人：|公司联系人：|：|暂未提供|未填写', '', text)[:3]
                text = re.sub(r'\s|\r|\n|\t|先生|女士|小姐|联系人：|公司联系人：|：|暂未提供|未填写', '', text)
                return text
            else:
                return text
        else:
            return ''

    # 清洗地址
    def search_address(self, text):
        if text:
            try:
                # '公司地址：中国  广东  广州  番禺区沙头街嘉品二街二号1栋1529'
                text = re.sub(r'\s|\r|\n|\t|地址|公司地址|公司地址：|：|暂未提供|未填写', '', text)
                return text
            except:
                return text
        else:
            return ''


if __name__ == '__main__':
    execute(["scrapy", "crawl", "b2b"])