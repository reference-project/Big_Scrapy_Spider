# # -*- coding: utf-8 -*-
# import scrapy
# import re
# import jieba.analyse
# from hashlib import md5
# from shijiegongchang.items import ShijiegongchangItem
# # from scrapy_redis.spiders import RedisSpider
# from scrapy.cmdline import execute
#
#
#
# class SjgcSpider(scrapy.Spider):
#     name = 'sjgc'
#     allowed_domains = ['company.ch.gongchang.com']
#     start_urls = ['https://company.ch.gongchang.com/']
#     # redis_key = "sjgc:start_urls"
#
#
#     def parse(self, response):
#         li_list = response.xpath("//div[@class='famous-company-list']//div[@class='famous-company-item']//ul//li//a")
#         for li in li_list:
#             kind_name = li.xpath("./text()").extract_first()
#             kind_href = li.xpath("./@href").extract_first()
#             if kind_href:
#                 kind_href = "https://company.ch.gongchang.com" + kind_href
#                 # print(kind_name,kind_href)
#                 yield scrapy.Request(
#                     url=kind_href,
#                     callback=self.parse_company_list,
#                     dont_filter=True
#                 )
#
#     def parse_company_list(self, response):
#         div_list = response.xpath("//div[@class='hot-company-city-list']//div[@class='hot-company-city-item']//a")
#         for div in div_list:
#             company_href = div.xpath("./@href").extract_first()
#             company_name = div.xpath("./@title").extract_first()
#             # company_address = "".join(div.xpath(".//dl//dd[contains(text(),'地址：')]/text()").extract())
#             # phone = div.xpath(".//span/text()").extract_first()
#             if company_href:
#                 company_href = "https:" + company_href
#                 # print(company_name,company_href)
#                 contact_href = company_href + "company_contact.html"
#                 yield scrapy.Request(
#                     url=contact_href,
#                     callback=self.parse_company_contact,
#                     dont_filter=True
#                 )
#
#         next_page_url = response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
#         if next_page_url:
#             next_page_url = "https://company.ch.gongchang.com" + next_page_url
#             yield scrapy.Request(
#                 url=next_page_url,
#                 callback=self.parse_company_list
#             )
#
#     def parse_company_contact(self, response):
#         item = ShijiegongchangItem()
#         pattern = re.compile(r'<dd><i class="icon-point"></i>地址：(.*?) </dd>',re.S)
#         pattern1 = re.compile(r'<div class="compony-info-name" com_name=".*?">(.*?)</div></dt>',re.S)
#         item["company_Name"] = "".join(re.findall(pattern1,response.text)) if re.findall(pattern1,response.text) else ""
#         item["kind"] = response.xpath("//div[@id='introbar']//dl//dd/text()").extract_first()
#         item["company_address"] = response.xpath("//dd[contains(text(),'地址')]/text()").extract_first()
#         item["linkman"] = "".join(response.xpath("//ul[@class='company-intro-list']//p[contains(text(),'联系人')]/..//text()").extract())
#         item["phone"] = "".join(response.xpath("//ul[@class='company-intro-list']//p[contains(text(),'手机')]/..//text()").extract())
#         item["telephone"] = "".join(response.xpath("//ul[@class='company-intro-list']//p[contains(text(),'联系电话')]/..//text()").extract())
#         item["contact_QQ"] = "".join(response.xpath("//ul[@class='side-info-list']//p[contains(text(),'QQ号')]/..//text()").extract())
#         if item["company_Name"]:
#             item["company_Name"] = item["company_Name"]
#         else:
#             try:
#                 item["company_Name"] = response.xpath("//div[@class='compony-info-name']/@com_name").extract_first()
#             except Exception as e:
#                 print(e)
#                 pass
#         item["company_id"] = md5(item["company_Name"].encode()).hexdigest()
#         if item["kind"]:
#             item["kind"] = re.sub(r'\s|\t|\r|\n|暂未提供|未填写|等', '', item["kind"]).replace(',', '|')\
#                 .replace(';','|').replace('、', '|').replace('，', '|').replace('；', '|').replace('/', '|')
#             item["kind"] = self.rinse_keywords(self.replace_ss(item["kind"]))
#         else:
#             item["kind"] = ''
#         item["Source"] = response.url
#         try:
#             item["province"] = "".join(re.findall(pattern, response.text)).split(' ')[0].replace('</dd>\n','') if re.findall(pattern, response.text) else ""
#             item["city_name"] = "".join(re.findall(pattern, response.text)).split(' ')[1].replace('</dd>\n','') if re.findall(pattern,response.text) else ""
#         except:
#             item["province"] = ''
#             item["city_name"] = ''
#         if item["company_address"]:
#             item["company_address"] = self.search_address(item["company_address"])
#         else:
#             item["company_address"] = ''
#         if item["linkman"]:
#             item["linkman"] = self.search_linkman(item["linkman"])
#         else:
#             item["linkman"] = ''
#         if item["phone"]:
#             item["phone"] = self.search_phone_num(item["phone"])
#         else:
#             item["phone"]= ''
#         if item["telephone"]:
#             item["telephone"] = self.search_telephone_num(item["telephone"])
#         else:
#             item["telephone"] = ''
#         if item["contact_QQ"]:
#             item["contact_QQ"] = self.search_QQ(item["contact_QQ"])
#         else:
#             item["contact_QQ"] = ''
#         yield item
#
#
#     # 处理行业关键字
#     def rinse_keywords(self, value):
#         result_list = []
#         for i in value.split('|'):
#             result_list.append(
#                 ''.join(jieba.analyse.extract_tags(i, topK=5, withWeight=False,
#                                                    allowPOS=('n', 'nz', 'v', 'vd', 'vn', 'l', 'a', 'd'))))
#         result = '|'.join(set([i for i in result_list if i]))
#         if result:
#             return result
#         else:
#             return ''
#
#     # replace 方法
#     def replace_ss(self, text, args=''):
#         if text:
#             args = list(args) + ['\r', '\n', ' ', '\t', '\xa0', '\u3000']
#             for i in args:
#                 text = text.replace(i, '')
#             return text
#         return ''
#
#     # 清洗手机
#     def search_phone_num(self, text):
#         if text:
#             try:
#                 pattern = re.compile(r'^1[35678]\d{9}$', re.S)
#                 text = re.sub(r'\s|\r|\t|\n|保密|移动电话：|电话：|未填写|无', '', text).strip()
#                 # text = re.search(r'1\d{10}',text).group(0)
#                 text = "".join(re.findall(pattern, text))
#                 return text
#             except:
#                 return ''
#         else:
#             return ''
#
#     # 清洗电话号码
#     def search_telephone_num(self, text):
#         if text:
#             try:
#                 pattern = re.compile(r'\(?0\d{2,3}[)-]?\d{7,8}', re.S)
#                 text = re.sub(r'\s|\r|\t|\n|公司电话：|：|暂未提供|未填写|无', '', text).strip()
#                 text = "".join(re.findall(pattern, text))
#                 return text
#             except:
#                 return ''
#         else:
#             return ''
#
#     # 清洗传真号码
#     def search_contact_Fax(self, text):
#         if text:
#             try:
#                 pattern = re.compile(r'\(?0\d{2,3}[)-]?\d{7,8}', re.S)
#                 # '公司联系人：胡'
#                 text = re.sub(r'\s|\r|\t|\n|公司传真：|：|暂未提供|未填写|无', '', text).strip()
#                 text = "".join(re.findall(pattern, text))
#                 return text
#             except:
#                 return ''
#         else:
#             return ''
#
#     # 清洗url
#     def search_url(self, text):
#         if text:
#             try:
#                 pattern = re.compile(
#                     r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|"
#                     r"([a-zA-Z]+.\w+\.+[a-zA-Z0-9\/_]+)", re.S)
#                 text = "".join(re.findall(pattern, text))
#                 return text
#             except:
#                 return ''
#
#         else:
#             return ''
#
#     # 清洗email
#     def search_email(self, text):
#         if text:
#             try:
#                 pattern = re.compile(r"[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+", re.S)
#                 text = re.sub(r'\s|\r|\t|\n|邮箱：|：|暂未提供|无', '', text).strip()
#                 text = "".join(re.findall(pattern, text))
#                 return text
#             except:
#                 return ''
#         else:
#             return ""
#
#     # 清洗QQ
#     def search_QQ(self, text):
#         if text:
#             try:
#                 pattern = re.compile(r"([1-9]\d{4,10})@qq.com|([1-9]\d{4,10})", re.S)
#                 text = re.sub(r'\s|\r|\t|\n|QQ：|：|暂未提供|未填写|无', '', text).strip()
#                 text = "".join(re.findall(pattern, text))
#                 return text
#             except:
#                 return ''
#         else:
#             return ''
#
#     # 清洗联系人
#     def search_linkman(self, text):
#         if text:
#             try:
#                 text = text.split(' ')[0].split('（')[0]
#                 # text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写', '', text)[:3]
#                 # text = re.sub(r'\s|\r|\n|\t|先生|女士|小姐|联系人：|公司联系人：|：|暂未提供|未填写', '', text)[:3]
#                 text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|无', '', text)
#                 return text
#             except:
#                 return ''
#         else:
#             return ''
#
#     # 清洗地址
#     def search_address(self, text):
#         if text:
#             try:
#                 text = text.split(' ')[-1]
#                 if text:
#                     text = re.sub(r'\s|\r|\n|\t|地址|公司地址|公司地址：|：|暂未提供|未填写|无', '', text)
#                     return text
#                 else:
#                     return ''
#             except:
#                 return ''
#         else:
#             return ''
#
#
#
#
#
#
# if __name__ == '__main__':
#     execute(["scrapy", "crawl", "sjgc"])
