# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Store(scrapy.Item):
    ID = scrapy.Field()
    CaseFrom = scrapy.Field()
    ContactStore = scrapy.Field()
    ContactStoreID = scrapy.Field()
    ContactTel = scrapy.Field()
    ContactUrl = scrapy.Field()
    ContactAddr = scrapy.Field()
    ContactFAX = scrapy.Field()
    ContactEMail = scrapy.Field()
    CaseSystem = scrapy.Field()
    District = scrapy.Field()
    City = scrapy.Field()


class Employee(scrapy.Item):
    ID = scrapy.Field()
    CaseFrom = scrapy.Field()
    City = scrapy.Field()
    District = scrapy.Field()
    ContactStoreID = scrapy.Field()
    ContactStore = scrapy.Field()
    EmpTitle = scrapy.Field()
    EmpName = scrapy.Field()
    EmpNameBinary = scrapy.Field()
    EmpMobile = scrapy.Field()
    EmpEMail = scrapy.Field()
    LicenseB = scrapy.Field()
    LicenseA = scrapy.Field()

