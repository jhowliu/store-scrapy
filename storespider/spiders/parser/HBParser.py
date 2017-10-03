# -*- coding=utf-8 -*-
import re
import hashlib
import logging

from bs4 import BeautifulSoup

from storespider.spiders.parser.template import StoreParser

class HBParser(StoreParser):

    def init(self):
        self.casefrom = 'HBHouse'
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def start_parse(self):
        store_infos = self.fill_out_webstored()
        emp_list = []

        tags = self.soup.select('ul.team-container li')

        for tag in tags:
            emp_list.append(self.fill_out_webagent(tag))

        return store_infos, emp_list

    def get_store_hash_id(self):
        hashid = hashlib.sha1('%s-%s-%s' % (self.casefrom, self.get_store_id(), self.date)).hexdigest()
        return hashid

    def get_store_link(self):
        return self.url

    def get_store_id(self):
        regex = re.compile('web\/([a-zA-Z0-9]+)\/')
        m = regex.search(self.url)
        store_id = m.group(1) if m else ''

        return store_id

    def get_store_name(self):
        tags = self.soup.select('div#MainContent_storeTitle')
        name = tags[0].text if len(tags) else ''

        return name

    def get_address(self):
        tags = self.soup.select('ul.base__info li')
        addr = tags[0].text.replace(u'地址：', '') if len(tags)>0 else ''

        return addr

    def get_tel_number(self):
        tags = self.soup.select('ul.base__info li')
        tel = tags[1].text.replace(u'電話：', '') if len(tags)>1 else ''

        return tel

    def get_fax_number(self):
        tags = self.soup.select('ul.base__info li')
        fax = tags[2].text.replace(u'傳真：', '') if len(tags)>2 else ''

        return fax

    def get_mail(self):
        tags = self.soup.select('ul.base__info li a')
        mail = tags[1]['href'].replace(' ','').replace('mailto:','') if len(tags)>1 else ''

        return mail

    def get_employee_hash_id(self, soup):
        concated = "%s-%s-%s" % (self.get_store_id(), self.get_employee_name(soup).encode('utf-8'), self.date)
        return hashlib.sha1(concated).hexdigest()

    def get_employee_name(self, soup):
        tags = soup.select('p.team__name')
        name = tags[0].text.replace(' ','').split('/')[0] if len(tags) else ''

        return name

    def get_employee_mail(self, soup):
        tags = soup.select('.btn-box a')
        mail = tags[0]['href'].replace('mailto:','') if len(tags) else ''

        return mail

    def get_employee_mobile(self, soup):
        tags = soup.select('div.team__contact p a')
        mobile = tags[0].text if len(tags)>0 else ''
        return mobile


    def get_employee_title(self, soup):
        tags = soup.select('p.team__name')
        title = tags[0].text.replace(' ','').split('/')[1] if len(tags) else u'營業員'

        return title
