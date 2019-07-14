# -*- coding: utf-8 -*-
import scrapy
import re
import jieba.analyse
from hashlib import md5
from makepolo.items import MakepoloItem
from scrapy_redis.spiders import RedisSpider
from scrapy.cmdline import execute



class MkplSpider(scrapy.Spider):
    name = 'mkpl'
    allowed_domains = ['china.makepolo.com','.cn.makepolo.com']
    start_urls = ['http://china.makepolo.com/']
    # redis_key = "mkpl:start_urls"

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
        "DOWNLOAD_HANDLERS": {
            'https': 'MkplSpider.custom.downloader.handler.https.HttpsDownloaderIgnoreCNError',
        },
    }

    def  start_requests(self):
        # start_urls = ['http://china.makepolo.com/']
        start_urls = self.start_urls[0]
        yield scrapy.Request(
            url=start_urls,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response):
        a_list = response.xpath("//div[@class='nav_con']//div[@class='sidebar_con']//div[@class='sidebar_con_title']//a")
        for a in a_list:
            kind_href = a.xpath("./@href").extract_first()
            kind_name = a.xpath("./text()").extract_first().replace('\xa0','')
            if kind_href:
                # print(kind_name,kind_href)
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_goods_list,
                    dont_filter=True
                )
    def parse_goods_list(self, response):
        company_lists_url = response.xpath("//div[@class='s_nav_tab']//a[contains(text(),'企业')]/@href").extract_first()
        if company_lists_url:
            company_lists_url = "http:" + company_lists_url
            # print(company_lists_url)
            yield scrapy.Request(
                url=company_lists_url,
                callback=self.parse_company_list,
                dont_filter=True
            )

    def parse_company_list(self, response):
        div_list = response.xpath("//div[@class='qi_ye_list clearfix']//div[@class='qi_box']")
        for div in div_list:
            company_Name = div.xpath(".//div[@class='qi_title']/a/text()").extract_first()
            company_link_href = div.xpath(".//div[@class='qi_b']//a[contains(text(),'查看联系方式')]/@href").extract_first()
            kinds = "".join(div.xpath(".//div[@class='qi_m']//span[contains(text(),'主营产品：')]/..//a/text()").extract())
            if kinds:
                kinds = re.sub(r'\s|\n|\r|\t|主营产品：','',kinds).replace(',','|')
            if company_link_href:
                company_link_href = "http:" + company_link_href
                # print(company_link_href)
                yield scrapy.Request(
                    url=company_link_href,
                    callback=self.parse_company_contact,
                    meta={"info": kinds},
                    dont_filter=True
                )
        next_page_url = response.xpath("//div[@class='nextpage']//a[contains(text(),' 下一页 > ')]/@href").extract_first()
        if next_page_url:
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_company_list,
                dont_filter=True
            )

    def parse_company_contact(self, response):
        kind = response.meta.get('info')
        item = MakepoloItem()
        pattern = re.compile(r'<meta content="(.*?)联系我们" name="keywords">',re.S)
        pattern1 = re.compile(r'<span class="num_l">(.*?)</span>',re.S)
        pattern2 = re.compile(r'<span class="num_r">(.*?)</span>',re.S)
        pattern3 = re.compile(r'<li>传真：(.*?)</li>', re.S)
        pattern4 = re.compile(r'<li>公司地址：(.*?)</li>', re.S)
        pattern5 = re.compile(r'<li>Email：(.*?)</li>', re.S)
        # <a href='http://sighttp.qq.com/msgrd?v=3&uin=994099506&site=qq&menu=yes' title="点击这里给我发QQ消息" class="onlineqq" target="_blank"><img src="http://jic.b2b.makepolo.com/img/yellow/yellow_new/qq.jpg" /> </a>
        # pattern6 = re.compile(r'<a href="http://sighttp.qq.com/msgrd?v=3&uin=(.*?)&site=qq&menu=yes" title=".*?" class="onlineqq" target="_blank"><img src=".*?" /> </a>')
        pattern6 = re.compile(r'uin=([1-9][0-9]{4,})&site')
        pattern7 = re.compile(r'<li>联系人：(.*?)</li>',re.S)
        pattern8 = re.compile('<div class="com_messages">所在地：(.*?)<br />')

        html_text = response.text
        if  html_text:
            try:
                item["company_Name"] = re.findall(pattern,html_text)[0]
                item["company_id"] = md5(item["company_Name"].encode()).hexdigest()
                item["linkman"] = "".join(re.findall(pattern7,html_text)).replace('暂无','').replace(' ','').replace('&nbsp','') if re.findall(pattern7,html_text) else None
                phone = "".join(re.findall(pattern1,html_text)).replace('暂无','') if re.findall(pattern1,html_text) else None
                telephone = "".join(re.findall(pattern2,html_text)).replace('暂无','') if re.findall(pattern2,html_text) else None
                contact_Fax = "".join(re.findall(pattern3,html_text)).replace('暂无','') if re.findall(pattern3,html_text) else None
                company_address = "".join(re.findall(pattern4,html_text)).replace('暂无','') if re.findall(pattern4,html_text) else None
                E_Mail = "".join(re.findall(pattern5, html_text)).replace('暂无','') if re.findall(pattern5,html_text) else None
                item["contact_QQ"] = "|".join(re.findall(pattern6, html_text)).split('|')[1] if re.findall(pattern6, html_text) else None
                item["province"] = "".join(re.findall(pattern8, html_text)).split(' ')[1] if re.findall(pattern8, html_text) else None
                item["city_name"] = "".join(re.findall(pattern8, html_text)).split(' ')[2] if re.findall(pattern8, html_text) else None
                if company_address:
                    item["company_address"] = re.sub('\s|\r|t|\n|公司地址：','',company_address).strip()
                else:
                    item["company_address"] = company_address
                if contact_Fax:
                    contact_Fax = re.sub('\s|\r|t|\n|传真：','',contact_Fax).strip()
                    item["contact_Fax"] = self.search_telephone_num(contact_Fax)
                else:
                    item["contact_Fax"] = contact_Fax
                item["phone"] = self.search_phone_num(phone)
                item["telephone"] = self.search_telephone_num(telephone)
                item["E_Mail"] = self.search_email(E_Mail)
                item["kind"] = self.rinse_keywords(self.replace_ss(kind))
                item["Source"] = response.url
                yield item
            except:
                return

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
                # text = re.search(r'1\d{10}',text).group(0)
                text = "".join(re.findall(pattern, text))
                return text
            except:
                return text
        else:
            return None

    # 清洗电话号码
    def search_telephone_num(self, text):
        if text:
            try:
                pattern = re.compile(r'\(?0\d{2,3}[)-]?\d{7,8}', re.S)
                text = "".join(re.findall(pattern, text))
                return text
            except:
                return text
        else:
            return None

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
                return text

        else:
            return None

    # 清洗email
    def search_email(self, text):
        if text:
            try:
                pattern = re.compile(r"[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+", re.S)
                text = "".join(re.findall(pattern, text))
                return text
            except:
                return text
        else:
            return ""

    # 清洗QQ
    def search_QQ(self, text):
        if text:
            try:
                pattern = re.compile(r"[1-9]\d{4,10}", re.S)
                text = "".join(re.findall(pattern, text))
                return text
            except:
                return text
        else:
            return None

    # 清洗联系人
    def search_linkman(self, text):
        if text:
            try:
                text = re.sub(r'\s|\r|\n|\t|先生|女士|小姐|联系人|：', '', text)[:3]
                return text
            except:
                return text
        else:
            return None

    # 清洗地址
    def search_address(self, text):
        if text:
            try:
                text = re.sub(r'\s|\r|\n|\t|地址|：', '', text)
                return text
            except:
                return text
        else:
            return None


if __name__ == '__main__':
    execute(["scrapy","crawl","mkpl"])