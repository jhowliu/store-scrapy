# -*- coding:utf-8 -*-
import scrapy
import math
import logging

from worker import Worker
from bs4 import BeautifulSoup

from scrapy.http import FormRequest

from storespider.spiders import config
from storespider.spiders.parser import CTParser, HBParser

from storespider.items import Store, Employee

class MainSpider(scrapy.Spider):
    name = 'web-store'

    def __init__(self, port=4445, *args, **kwargs):
        super(MainSpider, self).__init__(*args, **kwargs)
        self.worker = Worker(int(port))

    def start_requests(self):
        start_urls = {
            #'CTHouse': 'https://www.cthouse.com.tw/FranchiseList.aspx',
            #'Taiwan' : 'http://www.twhg.com.tw/stores.php',
            'HBHouse' : 'http://www.hbhousing.com.tw/franchise'
        }

        for store, url in start_urls.items():
            meta = { 'store': store }

            for city in config.CITIES:
                if store == 'CTHouse':
                    payload = config.CT_HOUSE_PAYLOAD
                    payload['arg'] = ('%s-city/' % city)

                    meta['payload'] = payload

                    yield FormRequest(url=url, callback=self.crawl_entries, \
                                formdata=payload, meta=meta)

                elif store == 'Taiwan':
                    page_url = '?'.join([url, 'city=%s'%city])
                    self.worker.get(page_url)
                    total = self.worker.execute_script('return $("span.total_page")[0].innerText')
                    final_page = math.ceil(int(total) / 10.0)

                    for i in range(1, int(final_page)):
                        logging.info('%s - %s - start crawling page: %d/%d' % (store, city, i, int(final_page)))
                        infos = self.worker.execute_script('return json_data')
                        meta['entries'] = infos
                        yield scrapy.Request(url=url, callback=self.crawl_entries, \
                                        meta=meta)
                        self.worker.execute_script('$(".pages_next")[0].click()')

            if  store == 'HBHouse':
                self.worker.get(url)
                final_page = self.worker.execute_script('return $("ul.base__list__pagenum li")[7].innerText')

                for i in range(1, int(final_page)):
                    logging.info('%s - start crawling page: %d/%d' % (store, i, int(final_page)))
                    html = self.worker.execute_script('return document.body.innerHTML')
                    if (not html): continue

                    meta['soup'] = BeautifulSoup(html, 'html.parser')

                    yield scrapy.Request(url=url, callback=self.crawl_entries, meta=meta, dont_filter=True)

                    click = self.worker.execute_script('$("ul.base__list__pagenum li:contains(\'%s\')")[0].click()' % '>')
                    if click == False:
                        self.worker.reopen()

            self.worker.close()


    def crawl_entries(self, response):
        meta = response.meta
        store = meta['store']

        if store == 'CTHouse':
            for entry in response.css('div.list div.n'):
                links = entry.css('a::attr(href)').extract()
                if len(links) > 1:
                    yield scrapy.Request(url=links[1], callback=self.parse_store, \
                                    meta=meta)

        elif store == 'Taiwan':
            entries = meta['entries']
            for entry in entries:
                meta['infos'] = entry
                yield scrapy.Request(url=entry['url'], callback=self.parse_store, \
                                meta=meta)

        elif store == 'HBHouse':
            soup = meta['soup']
            entries = soup.select('div.base__header__tit a')
            for entry in entries:
                url = ''.join([config.HBHOUSE_STORE_HOST, entry['href']])
                yield scrapy.Request(url=url, callback=self.parse_store, meta=meta)

    def parse_store(self, response):
        store = response.meta['store']
        logging.info('%s - %s' % (store, response.url))

        if store == 'CTHouse':
            store, emp_list = CTParser(response.body, response.url).start_parse()

        elif store == 'Taiwan':
            print(response.meta['infos']['Name'])

        elif store == 'HBHouse':
            store, emp_list = HBParser(response.body, response.url).start_parse()

        yield Store(store)
        for emp in emp_list:
            yield Employee(emp)

