import logging

from storespider.orm.engine import sess
from storespider.orm.schema import WebAgent, WebStore
def insert_store(item):

    logging.info("<INSERT STORE> - %s" % item['ID'])

    value = WebStore(idx=item['ID'],
                     KeyinDate=item['DateTime'],
                     CaseFrom=item['CaseFrom'],
                     CaseSystem=item['CaseSystem'],
                     ContactStore=item['ContactStore'],
                     ContactStoreID=item['ContactStoreID'],
                     ContactTel=item['ContactTel'],
                     ContactFAX=item['ContactFAX'],
                     ContactUrl=item['ContactUrl'],
                     ContactAddr=item['ContactAddr'],
                     ContactEMail=item['ContactEMail'],
                     City=item['City'],
                     District=item['District'])

    row = sess.query(WebStore).filter_by(idx=item['ID']).first()

    if (not row):
        sess.add(value)
        sess.commit()

def insert_employee(item):

    logging.info("<INSERT AGENT> - %s" % item['ID'])

    value = WebAgent(id=item['ID'],
                     KeyinDate=item['DateTime'],
                     CaseFrom=item['CaseFrom'],
                     ContactStore=item['ContactStore'],
                     ContactStoreID=item['ContactStoreID'],
                     EmpTitle=item['EmpTitle'],
                     EmpName=item['EmpName'],
                     EmpMobile=item['EmpMobile'],
                     EmpEMail=item['EmpEMail'],
                     LicenseB=item['LicenseB'],
                     City=item['City'],
                     District=item['District'])

    row = sess.query(WebAgent).filter_by(id=item['ID']).first()

    if (not row):
        sess.add(value)
        sess.commit()

