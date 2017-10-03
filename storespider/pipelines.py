# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from storespider.items import Employee, Store
from storespider.orm.control import insert_store, insert_employee

class StorespiderPipeline(object):
    def process_item(self, item, spider):

        if type(item) == Store:
            insert_store(item)
        else:
            insert_employee(item)

        return item
