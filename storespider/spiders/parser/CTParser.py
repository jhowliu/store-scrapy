# -*- coding=utf-8 -*-
import re
import hashlib
import logging

from bs4 import BeautifulSoup

from storespider.spiders.parser.template import StoreParser

class CTParser(StoreParser):

    def init(self):
        self.casefrom = 'CTHouse'
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def start_parse(self):
        store_infos = self.fill_out_webstored()
        emp_list = []

        tags = self.soup.select('div.bestTeam li')
        for tag in tags:
            emp_list.append(self.fill_out_webagent(tag))

        return store_infos, emp_list

    def get_store_hash_id(self):
        hashid = hashlib.sha1('%s-%s-%s' % (self.casefrom, self.get_store_id(), self.date)).hexdigest()
        return hashid

    def get_store_link(self):
        return self.url

    def get_store_id(self):
        regex = re.compile('/([0-9]+)/')
        m = regex.search(self.url)

        return m.group(1) if m else ""

    def get_store_name(self):
        tags = self.soup.select('div.storeName')
        name = tags[0].text if len(tags) else ""
        logging.info('<CTHouse> - Store name - %s' % name)

        return name

    def get_address(self):
        tags = self.soup.select('div.info span.addr')
        addr = tags[0].text if len(tags) else ""
        logging.info('<CTHouse> - Store address - %s' % addr)

        return addr

    def get_tel_number(self):
        tags = self.soup.select('div.info span.tel')
        tel = tags[0].text if len(tags) else ""
        logging.info('<CTHouse> - Store tel - %s' % tel)

        return tel

    def get_mail(self):
        pass

    def get_fax_number(self):
        tags = self.soup.select('div.info span.tel')
        fax = tags[0].text if len(tags) else ""
        logging.info('<CTHouse> - Store fax - %s' % fax)

        return fax

    def get_case_system(self):
        pass

    def get_employee_hash_id(self, soup):
        concated = "%s-%s-%s" % (self.get_store_id(), self.get_employee_name(soup).encode('utf-8'), self.date)
        return hashlib.sha1(concated).hexdigest()

    def get_employee_name(self, soup):
        tags = soup.select('b')
        name = tags[0].text.strip() if len(tags) else ""
        logging.info('<CTHouse> - Employee name - %s' % name)

        return name

    def get_employee_mail(self, soup):
        pass

    def get_employee_mobile(self, soup):
        tags = soup.select('a.on')
        mobile = tags[0]['mobile'] if len(tags) else ""
        logging.info('<CTHouse> - Employee mobile - %s' % mobile)

        return mobile

    def get_employee_license(self, soup):
        pass

    def get_employee_title(self, soup):
        return u'營業員'
