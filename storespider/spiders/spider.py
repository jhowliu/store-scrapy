# -*- coding=utf-8 -*-
import scrapy

from scrapy.http import FormRequest
from storespider.spiders import config

class MainSpider(scrapy.Spider):
    name="web-store"

    def start_requests(self):
        start_urls = {
            "CTHouse": "https://www.cthouse.com.tw/FranchiseList.aspx"
        }

        for store, url in start_urls.items():
            if store == "CTHouse":
                payload = config.CT_HOUSE_PAYLOAD

                for city in config.CITIES:
                    payload['arg'] = ("%s-city/" % city)
                    yield FormRequest(url=url, callback=self.crawl_entities, \
                                formdata=payload)


    def crawl_entities(self, response):
        print(response.body)
