# -*- coding:utf-8 -*-
import re
import hashlib
import logging
import requests

from bs4 import BeautifulSoup

from storespider.spiders.parser.template import StoreParser

class TWParser(StoreParser):

    def init(self):
        self.casefrom = 'Taiwan'
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def start_parse(self):
        store_infos = self.fill_out_webstored()
        emp_list = []

        res = requests.get(self.url+'person')
        res.encoding='utf-8'
        if res.status_code != 200:
            return store_infos, emp_list

        soup = BeautifulSoup(res.text, 'html.parser')
        tags = soup.select('ul.group li')

        for tag in tags:
            emp_list.append(self.fill_out_webagent(tag))

        return store_infos, emp_list

    def get_store_hash_id(self):
        hashid = hashlib.sha1('%s-%s-%s' % (self.casefrom, self.get_store_id(), self.date)).hexdigest()
        return hashid

    def get_store_link(self):
        return self.url

    def get_store_id(self):
        regex = re.compile('stores\/([a-zA-Z0-9]+)\/')
        m = regex.search(self.url)
        store_id = m.group(1) if m else ''

        return store_id

    def get_store_name(self):
        tags = self.soup.select('span.slogan')
        name = tags[0].text if len(tags) else ''

        return name

    def get_address(self):
        tags = self.soup.select('div.store_name h3')
        addr = tags[0].text.split('\t')[-1] if len(tags) else ''

        return addr

    def get_tel_number(self):
        tags = self.soup.select('div.store_name span a')
        tel = tags[0].text if len(tags) else ''

        return tel

    def get_fax_number(self):
        return self.get_tel_number()

    def get_case_system(self):
        addr = self.get_address()
        tags = self.soup.select('div.store_name h3')
        case_system = tags[0].text.replace(addr, '') if len(tags) else ''
        return re.sub('\t|\n| ', '', case_system)

    def get_employee_hash_id(self, soup):
        concated = "%s-%s-%s" % (self.get_store_id(), self.get_employee_name(soup).encode('utf-8'), self.date)
        return hashlib.sha1(concated).hexdigest()

    def get_employee_name(self, soup):
        tags = soup.select('div.information h2')
        name = tags[0].text.split()[0] if len(tags) else ''

        return name

    def get_employee_mail(self, soup):
        tags = soup.select('div.infotel span a')
        mail = tags[0]['href'].replace('mailto:','') if len(tags) else ''

        return mail

    def get_employee_mobile(self, soup):
        tags = soup.select('div.infotel span')
        mobile = tags[0].text if len(tags)>0 else ''
        mobile = mobile.split()[-1].replace('M', '')

        return mobile

    def get_employee_title(self, soup):
        tags = soup.select('p.information h2')
        title = tags[0].text.split()[1] if len(tags) else u'營業員'

        return title
