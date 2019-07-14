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
# class SjgcSpider(scrapy.Spider):
#     name = 'sjgc'
#     allowed_domains = ['ch.gongchang.com']
#     start_urls = ['https://ch.gongchang.com/']
#     # redis_key = "sjgc:start_urls"
#     #
#     # def start_requests(self):
#     #     start_urls = 'https://ch.gongchang.com/'
#     #     yield scrapy.Request(
#     #         url=start_urls,
#     #         callback=self.parse
#     #     )
#
#
#     def parse(self, response):
#         div_list = response.xpath("//div[@class='main layout']//div[@class='cate-floor clearfix']//div[@class='sub-cate-list-wrap clearfix']//dl//dd//a")
#         for div in div_list:
#             kind_name = div.xpath("./text()").extract_first()
#             kind_href = div.xpath("./@href").extract_first()
#             if kind_href:
#                 kind_href = "https:" + kind_href
#                 # print(kind_name,kind_href)
#                 yield scrapy.Request(
#                     url=kind_href,
#                     callback=self.parse_kind_list,
#                     dont_filter=True
#                 )
#
#     def parse_kind_list(self, response):
#         li_list = response.xpath("//div[@class='left-content']//ul[@class='pro-classify-group clearfix']//li//a")
#         for li in li_list:
#             s_kind_name = li.xpath("./text()").extract_first()
#             s_kind_href = li.xpath("./@href").extract_first()
#             if s_kind_href:
#                 # '//qiche.ch.gongchang.com/zhuanyongqiche/chuishiche/'
#                 try:
#                     base_url = "https://" + s_kind_href.split('/')[2]
#                     s_kind_href = "https:" + s_kind_href
#                     yield scrapy.Request(
#                         url=s_kind_href,
#                         callback=self.parse_company_list,
#                         meta={"info1": base_url},
#                         dont_filter=True
#                     )
#                 except:
#                     return
#
#     def parse_company_list(self, response):
#         base_url = response.meta.get("info1")
#         a_list = response.xpath("//div[@class='message-content']/ul//li[@class='msg-item']//div[@class='pro-intro']//a[@class='company-name']")
#         for a in a_list:
#             company_href = a.xpath("./@href").extract_first()
#             company_name = a.xpath("./text()").extract_first()
#             if company_href:
#                 company_href = "https:" + company_href
#                 yield scrapy.Request(
#                     url=company_href,
#                     callback=self.parse_company_detail,
#                     dont_filter=True
#                 )
#         next_page_url = response.xpath("//div[@class='msg-footer']//a[contains(text(),'下一页')]/@href").extract_first()
#         if next_page_url:
#             try:
#                 next_page_url = base_url + next_page_url
#                 yield scrapy.Request(
#                     url=next_page_url,
#                     callback=self.parse_company_list,
#                     dont_filter=True
#                 )
#             except:
#                 return
#
#
#     def parse_company_detail(self, response):
#         kinds = "".join(response.xpath("//ul[@class='side-info-list']//p[contains(text(),'主营产品：')]/..//text()").extract())
#         if kinds:
#             kinds = re.sub(r'\s|\r|\t|\n|主营产品：|无','',kinds).strip()
#         address = "".join(response.xpath("//ul[@class='side-info-list']//p[contains(text(),'公司地址：')]/..//text()").extract())
#         if address:
#             address = re.sub(r'\s|\r|\t|\n|公司地址：|无','',address).strip()
#         contact_href = response.xpath("//div[@id='nav']//a[contains(text(),'联系我们')]/@href").extract_first()
#         if contact_href:
#             contact_href = "https:" + contact_href
#             yield scrapy.Request(
#                 url=contact_href,
#                 callback=self.parse_company_contact,
#                 meta={"info": kinds},
#                 dont_filter=True
#             )
#
#     def parse_company_contact(self, response):
#         item = ShijiegongchangItem()
#         pattern = re.compile(r'<dd><i class="icon-point"></i>地址：(.*?) </dd>',re.S)
#         pattern1 = re.compile(r'<div class="compony-info-name" com_name=".*?">(.*?)</div></dt>',re.S)
#         # item["company_Name"] = response.xpath("//ul[@class='company-intro-list']//p[contains(text(),'公司名称')]/../text()").extract_first()
#         item["company_Name"] = "".join(re.findall(pattern1,response.text)) if re.findall(pattern1,response.text) else ""
#         item["company_id"] = md5(item["company_Name"].encode()).hexdigest()
#         item["kind"] = response.meta.get("info")
#         item["Source"] = response.url
#         try:
#             item["province"] = "".join(re.findall(pattern, response.text)).split(' ')[0].replace('</dd>\n','') if re.findall(pattern, response.text) else ""
#             item["city_name"] = "".join(re.findall(pattern, response.text)).split(' ')[1].replace('</dd>\n','') if re.findall(pattern,response.text) else ""
#         except:
#             item["province"] = ''
#             item["city_name"] = ''
#         company_address = response.xpath("//dd[contains(text(),'地址')]/text()").extract_first()
#         linkman = "".join(response.xpath("//ul[@class='company-intro-list']//p[contains(text(),'联系人')]/..//text()").extract())
#         phone = "".join(response.xpath("//ul[@class='company-intro-list']//p[contains(text(),'手机')]/..//text()").extract())
#         telephone = "".join(response.xpath("//ul[@class='company-intro-list']//p[contains(text(),'联系电话')]/..//text()").extract())
#         contact_QQ = "".join(response.xpath("//ul[@class='side-info-list']//p[contains(text(),'QQ号')]/..//text()").extract())
#
#         if company_address:
#             item["company_address"] = self.search_address(company_address)
#         if linkman:
#             item["linkman"] = self.search_linkman(linkman)
#         if phone:
#             item["phone"] = self.search_phone_num(phone)
#         if telephone:
#             item["telephone"] = self.search_telephone_num(telephone)
#         if contact_QQ:
#             item["contact_QQ"] = self.search_QQ(contact_QQ)
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
#                 text = re.sub(r'\s|\t|\r|\n|手机|：', '', text).strip()
#                 pattern = re.compile(r'^1[35678]\d{9}$', re.S)
#                 # text = re.search(r'1\d{10}',text).group(0)
#                 text = "".join(re.findall(pattern, text))
#                 return text
#             except:
#                 return text
#         else:
#             return None
#
#     # 清洗电话号码
#     def search_telephone_num(self, text):
#         if text:
#             try:
#                 text = re.sub(r'\s|\t|\r|\n|电话|联系电话|：','',text).strip()
#                 pattern = re.compile(r'\(?0\d{2,3}[)-]?\d{7,8}', re.S)
#                 text = "".join(re.findall(pattern, text))
#                 return text
#             except:
#                 return text
#         else:
#             return None
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
#                 return text
#
#         else:
#             return None
#
#     # 清洗email
#     def search_email(self, text):
#         if text:
#             try:
#                 pattern = re.compile(r"[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+", re.S)
#                 text = "".join(re.findall(pattern, text))
#                 return text
#             except:
#                 return text
#         else:
#             return None
#
#     # 清洗QQ
#     def search_QQ(self, text):
#         if text:
#             try:
#                 pattern = re.compile(r"[1-9]\d{4,10}", re.S)
#                 text = "".join(re.findall(pattern, text))
#                 return text
#             except:
#                 return text
#         else:
#             return None
#
#     # 清洗联系人
#     def search_linkman(self, text):
#         if text:
#             try:
#                 text = re.sub(r'\s|\r|\n|\t|先生|女士|小姐|联系人|：', '', text)[:3]
#                 return text
#             except:
#                 return text
#         else:
#             return None
#
#     # 清洗地址
#     def search_address(self, text):
#         if text:
#             try:
#                 text = re.sub(r'\s|\r|\n|\t|地址|：', '', text)
#                 return text
#             except:
#                 return text
#         else:
#             return None
#
#
#
#
#
#
# if __name__ == '__main__':
#     execute(["scrapy", "crawl", "sjgc"])
