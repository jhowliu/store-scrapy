import sys
import time
import hashlib

from schema import WEB_STORED
from schema import WEB_AGENT

class StoreParser(object):
    def __init__(self, html=None):
        self.date = time.strftime("%Y-%m-%d")
        self.html = html
        self.init()

    def init(self):
        pass

    def start_parse(self):
        self.fill_out_webstored()
        #self.fill_out_webagent()

    # employee primary key
    def _employee_hash_id(self):
        concated = "%s:%s:%s" % (self.store_id, self.emp_name, self.date)
        return hashlib.sha1(concated).hexdigest()

    def get_store_hash_id(self):
        pass
    def get_store_link(self):
        pass
    def get_store_id(self):
        pass
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
    def get_employee_links(self, store_link):
        pass
    def get_employee_name(self, soup):
        pass
    def get_employee_mail(self, soup):
        pass
    def get_employee_mobile(self, soup):
        pass
    def get_employee_license(self, soup):
        pass
    def get_employee_title(self, soup):
        pass
    def parse_employee_info(self):
        pass

    def get_splited_address(self):
        addr = self.get_address()
        splited_addr = SPLIT_ADDR(addr.encode('utf-8'))

        city = splited_addr[0].decode('utf-8') if len(splited_addr)>0 else ""
        district = splited_addr[1].decode('utf-8') if len(splited_addr)>1 else ""

        return city, district


    def fill_out_webstored(self):

        # WEB_STORED
        #city, district = self.get_splited_address()
        WEB_STORED['idx'] = self.get_store_hash_id()
        WEB_STORED['CaseFrom'] = self.casefrom
	WEB_STORED['ContactStore'] = self.get_store_name()
	WEB_STORED['ContactStoreID'] = self.get_store_id()
	WEB_STORED['ContactTel'] = self.get_tel_number()
	WEB_STORED['ContactUrl'] = self.get_store_link()
	WEB_STORED['ContactAddr'] = self.get_address()
	WEB_STORED['CaseSystem'] = self.get_case_system()
        WEB_STORED['ContactFAX'] = self.get_fax_number()
        WEB_STORED['ContactEMail'] = self.get_mail()
	WEB_STORED['District'] = district
	WEB_STORED['City'] = city
        #print(WEB_STORED)
	#self.commit.sendDatabaseRemote(WEB_STORED, time.time())


    def fill_out_webagent(self, soup):
        # WEB_AGENT

	WEB_AGENT['WebAgent']['id'] = self._employee_hash_id()
        WEB_AGENT['WebAgent']['CaseFrom'] = self.casefrom
	WEB_AGENT['WebAgent']['ContactStore'] = self.get_store_name()
	WEB_AGENT['WebAgent']['ContactStoreID'] = self.get_store_id()
	WEB_AGENT['WebAgent']['EmpName'] = self.get_employee_name(soup)
	WEB_AGENT['WebAgent']['EmpMobile'] = self.get_employee_mobile(soup)
	WEB_AGENT['WebAgent']['EmpEMail'] = self.get_employee_mail(soup)
	WEB_AGENT['WebAgent']['EmpTitle'] = self.get_employee_title(soup)
	WEB_AGENT['WebAgent']['LicenseB'] = self.get_employee_license(soup)
	WEB_AGENT['WebAgent']['District'] = WEB_STORED['WebStored']['District']
	WEB_AGENT['WebAgent']['City'] = WEB_STORED['WebStored']['City']

        #print(WEB_AGENT)
	#self.commit.sendDatabaseRemote(WEB_AGENT, time.time())
