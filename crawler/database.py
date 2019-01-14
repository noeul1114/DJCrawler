""":mod:`crawler.database` ---  MongoDB Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import logging

import psycopg2 as pg2


from .config import crawler_config_mongo as crawler_config
from .config import crawler_config_postgres as crawler_config_postgres


logger = logging.getLogger(__name__)


class PostgresDB:
    def __init__(self, db: str):
        self.db_name = 'crawler'
        self.db_id = 'postgres'
        self.db_pw = 'qudtlstz1'
        self.db_host = 'localhost'
        self.cur = None

    def connect(self):
        try:
            conn = pg2.connect('host=localhost user=postgres dbname=test password=qudtlstz1')
        except:
            conn = pg2.connect('host=localhost user=postgres password=qudtlstz1')

            conn.autocommit = True
            cur = conn.cursor()

            cur.execute('create database test')
            cur.execute('SELECT version()')

            cur.execute('create table archive (id serial PRIMARY KEY, type varchar,  link varchar , count integer ,\
                         title varchar , date timestamp , article text)')

            conn.close()

            conn = pg2.connect('host=localhost user=postgres dbname=test password=qudtlstz1')

        conn.autocommit = True
        self.cur = conn.cursor()

    def query(self, document: str):
        self.cur.execute()

