""":mod:`crawler.worker.ruliweb` ---  Crawler for Ruliweb
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import logging

from .base import BaseSite
from ..exc import SkipCrawler
from ..serializers import payload_serializer
logger = logging.getLogger(__name__)


class RuliwebHotdeal(BaseSite):

    def __init__(self, *, threshold=15, page_max=20):
        BaseSite.__init__(self)
        self.threshold = threshold
        self.pageMax = page_max

    def crawler(self):
        l = logger.getChild('RuliwebHotdeal.crawler')
        for page in range(1, self.pageMax, 1):
            host = 'http://bbs.ruliweb.com/market/board/1020'
            query = 'page={}'.format(page, page)
            self.url = '{host}?{query}'.format(host=host, query=query)
            soup = self.crawling(self.url)
            if soup is None:
                l.error('{} crawler skip'.format(self.type))
                raise SkipCrawler
            yield soup

    def articler(self, link):
        l = logger.getChild('Ruliweb_hotdeal.articler')
        soup = self.crawling(link)
        if soup is None:
            l.error('{} crawler skip'.format(self.type))
            raise SkipCrawler
        return soup

    def do(self):
        l = logger.getChild('RuliwebHotdeal.do')
        l.info('start {} crawler'.format(self.type))
        for soup in self.crawler():
            for ctx in soup.select('tbody tr'):
                tr_class = ctx.attrs['class']
                if len(tr_class) == 2 and tr_class[1] == "notice":
                    continue
                _temp = ctx.select("td.hit")
                _count = int(_temp[0].text)
                if _count >= self.threshold:
                    _title = ctx.select('a')[1].text
                    _link = ctx.select('a')[1].get('href')

                    article_soup = self.articler(_link)
                    _article = article_soup.find('div', {"class": "view_content"})

                    obj = payload_serializer(type=self.type, link=_link,
                                             count=_count, title=_title, article=_article)
                    self.django_insert_update(obj)
                    # self.insert_or_update_postgres(obj)
