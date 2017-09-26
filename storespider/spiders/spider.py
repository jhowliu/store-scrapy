# -*- coding=utf-8 -*-
import scrapy
import logging

from scrapy.http import FormRequest

from storespider.spiders import config
from storespider.spiders.parser import CTParser

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
            for entry in response.css('div.list div.n'):
                links = entry.css('a::attr(href)').extract()
                if len(links) > 1:
                    yield scrapy.Request(url=links[1], callback=self.parse_page, \
                                meta=response.meta)


    def parse_page(self, response):
        logging.info(response.url)
        store = response.meta['store']

        if store == 'CTHouse':
           CTParser(response.body).start_parse()

