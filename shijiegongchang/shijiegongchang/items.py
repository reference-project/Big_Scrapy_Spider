# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShijiegongchangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO shijiegongchang_2019_06_23(
                            company_Name,company_id,kind,linkman,phone,telephone,contact_QQ,province,city_name,
                            company_address,Source
                            ) 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                            ON DUPLICATE KEY UPDATE 
                            company_Name=VALUES(company_Name),
                            company_id=VALUES(company_id),
                            kind=VALUES(kind),
                            linkman=VALUES(linkman),
                            phone=VALUES(phone),
                            telephone=VALUES(telephone),
                            contact_QQ=VALUES(contact_QQ),
                            province=VALUES(province),
                            city_name=VALUES(city_name),
                            company_address=VALUES(company_address),
                            Source=VALUES(Source)
                            """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['contact_QQ'], self['province'], self['city_name'],
            self['company_address'], self['Source']
        )

        return sql, params
