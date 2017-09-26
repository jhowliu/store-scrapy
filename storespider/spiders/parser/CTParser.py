import re
import hashlib
import logging

from bs4 import BeautifulSoup
from storespider.spiders.parser.template import StoreParser

class CTParser(StoreParser):

    def init(self):
        self.casefrom = 'CTHouse'
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def get_store_hash_id(self):
        hashid = hashlib.sha1("%s-%s-%s" % (self.casefrom, self.get_store_id(), self.date)).hexdigest()
        return hashid

    def get_store_link(self):
        link = self.soup.select('div.n a')[1]['href']
        return link

    def get_store_id(self):
        regex = re.compile('/([0-9]+)/')
        link = self.get_store_link()
        m = regex.search(link)
        return m.group(1) if m else ""

    def get_store_name(self):
        pass

    def get_address(self):
        pass

    def get_tel_number(self):
        pass

    def get_mail(self):
        pass

    def get_fax_number(self):
        pass

    def get_case_system(self):
        pass

