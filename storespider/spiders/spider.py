# -*- coding=utf-8 -*-
import scrapy
import logging

from scrapy.http import FormRequest

from storespider.spiders import config
from storespider.spiders.parser import CTParser

from storespider.items import Store, Employee

class MainSpider(scrapy.Spider):
    name = 'web-store'

    def start_requests(self):
        start_urls = {
            'CTHouse': 'https://www.cthouse.com.tw/FranchiseList.aspx'
        }

        for store, url in start_urls.items():
            if store == 'CTHouse':
                payload = config.CT_HOUSE_PAYLOAD
                meta = { 'store': store, 'payload': payload }

                for city in config.CITIES[:2]:
                    payload['arg'] = ('%s-city/' % city)
                    yield FormRequest(url=url, callback=self.crawl_entities, \
                                formdata=payload, meta=meta)


    def crawl_entities(self, response):
        store = response.meta['store']

        if store == 'CTHouse':
            for entry in response.css('div.list div.n')[:1]:
                links = entry.css('a::attr(href)').extract()
                if len(links) > 1:
                    yield scrapy.Request(url=links[1], callback=self.parse_store, \
                                meta=response.meta)

    def parse_store(self, response):
        store = response.meta['store']
        logging.info('%s - %s' % (store, response.url))

        if store == 'CTHouse':
           store, emp_list = CTParser(response.body, response.url).start_parse()

           yield Store(store)
           for emp in emp_list:
               yield Employee(emp)


