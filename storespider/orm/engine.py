from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# [driver]://user:password@host/dbname
engine = create_engine('mysql://lingtelli:lingtellimi4ma3@192.168.10.14/WebEXTDW?charset=utf8', encoding='utf-8')


Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

sess = Session()
