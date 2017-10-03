import logging

from storespider.orm.engine import sess
from storespider.orm.schema import WebAgent, WebStore

def insert_store(item):
    logging.info("<INSERT STORE> - %s" % item['idx'])

    value = WebStore(**item)
    row = sess.query(WebStore).filter_by(idx=item['idx']).first()

    if (not row):
        sess.add(value)
        sess.commit()

def insert_employee(item):
    logging.info("<INSERT AGENT> - %s" % item['id'])

    value = WebAgent(**item)
    row = sess.query(WebAgent).filter_by(id=item['id']).first()

    if (not row):
        sess.add(value)
        sess.commit()

