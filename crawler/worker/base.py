""":mod:`crawler.worker.base` ---  Crawler Base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import logging
import datetime
import sys

from urllib.error import URLError
from urllib.request import Request, urlopen

import psycopg2 as pg2
from django.utils import timezone

from pasted.models import PastedData

from bs4 import BeautifulSoup

from ..config import crawler_config_mongo as crawler_config
from ..database import PostgresDB

sys.path.append("..")


logger = logging.getLogger(__name__)


class BaseSite:

    def __init__(self):
        # self.db = MongoDB('test_crawler')
        self.db = PostgresDB('community_crawler')

    @property
    def type(self):
        return self.__class__.__name__

    def insert_or_update(self, data):
        l = logger.getChild('BaseSite.insert_or_update')
        l.info('insert data: {}'.format(data))
        document = 'archive'

        objid = None
        c = self.db.query(document) \
            .find_one({'type': data['type'],
                       'id': data['id']})
        if data.get('id') is None:
            c = self.db.query(document) \
                .find_one({'type': data['type'],
                           'title': data['title']})
        if c is None:
            objid = self.db.insert(document, data=data)
            l.info('insert data: {}, objid: {}'.format(data, objid))
        else:
            if int(c['count']) < int(data['count']):
                l.info('update objid: {}, count {}->{}'
                       .format(c['_id'], c['count'], data['count']))
                d = {'count': data['count'], 'date': data['date']}
                objid = self.db.update(document, c=c, data=d)
                if objid['ok']:
                    return c['_id']
        return objid

    def insert_or_update_postgres(self, data):
        l = logger.getChild('BaseSite.insert_or_update')
        l.info('insert data: {}'.format(data))

        conn = pg2.connect('host=localhost user=postgres dbname=test password=qudtlstz1')

        cur = conn.cursor()
        objid = None

        cur.execute("SELECT * FROM archive WHERE type=%s AND id=%s", (data['type'], data['id']))
        c = cur.fetchone()
        if data.get('id') is None:
            cur.execute('SELECT * FROM archive WHERE type = %s AND title = %s;' , (data['type'], data['title']))
            c = cur.fetchone()
        if c is None:
            objid = cur.execute('INSERT INTO archive(type, link, count, title, date, article) VALUES(%s, %s, %s, %s, %s, %s)',
                                (data['type'], data['link'], data['count'], data['title'], datetime.datetime.now(), data['article']))
            conn.commit()
            conn.close()
            l.info('insert data: {}, objid: {}'.format(data, objid))
        # else:
        #     if int(c['count']) < int(data['count']):
        #         l.info('update objid: {}, count {}->{}'
        #                .format(c['_id'], c['count'], data['count']))
        #         d = {'count': data['count'], 'date': data['date']}
        #         objid = cur.execute(, c=c, data=d)
        #         if objid['ok']:
        #             return c['_id']
        return objid

    def crawling(self, url, encoding='utf-8'):
        l = logger.getChild('BaseSite.crawling')
        request = Request(url, headers={
            'User-Agent':
                'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) '
                'Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'})
        try:
            handle = urlopen(request)
        except URLError:
            l.error('may be, url host changed: {}'.format(url))
            return None
        data = handle.read()
        soup = BeautifulSoup(data, "html.parser", from_encoding=encoding)
        return soup

    def django_insert_update(self, data):
        l = logger.getChild('BaseSite.insert_or_update')
        tag_soup = BeautifulSoup(str(data['article']), features="html.parser")
        try:
            tag_soup.div.unwrap()
            tag_soup = BeautifulSoup(str(tag_soup), features="html.parser")
            tag_soup.html.unwrap()
            tag_soup = BeautifulSoup(str(tag_soup), features="html.parser")
            tag_soup.body.unwrap()
            tag_soup = BeautifulSoup(str(tag_soup), features="html.parser")
            tag_soup.head.decompose()
        except:
            pass

        data['article'] = str(tag_soup)

        if len(PastedData.objects.filter(title=data['title'], type=self.type)) == 0:
            try:
                Data = PastedData.objects.create(title=data['title'],
                                                 type=self.type,
                                                 article=data['article'],
                                                 link=data['link'],
                                                 count=data['count'],
                                                 first_pasted=timezone.now(),
                                                 )
                Data.save()
                l.info('insert data: {}'.format(data))
            except:
                l.info('insert data failed')
                pass
        else:
            l.info('Data Already Pasted!!! title = {}'.format(data['title']))
            pass
