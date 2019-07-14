# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class B2B168Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    # E_Mail = scrapy.Field()
    contact_QQ = scrapy.Field()
    # province = scrapy.Field()
    # city_name = scrapy.Field()
    company_address = scrapy.Field()
    contact_Fax = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO makepolo_2019_06_22(
                            company_Name,company_id,kind,linkman,phone,telephone,contact_QQ,
                            company_address,contact_Fax,Source
                            ) 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                            ON DUPLICATE KEY UPDATE 
                            company_Name=VALUES(company_Name),
                            company_id=VALUES(company_id),
                            kind=VALUES(kind),
                            linkman=VALUES(linkman),
                            phone=VALUES(phone),
                            telephone=VALUES(telephone),
                            contact_QQ=VALUES(contact_QQ),
                            company_address=VALUES(company_address),
                            contact_Fax=VALUES(contact_Fax),
                            Source=VALUES(Source)
                            """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'], self['phone'],
            self['telephone'], self['contact_QQ'], self['company_address'], self['contact_Fax'], self['Source']
        )

        return sql, params
