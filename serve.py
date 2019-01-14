""":mod:`crawler.serve` ---  Crawler thread context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import logging.config
import random
import threading
import os

# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_crawler.settings")
# 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()

from datetime import datetime, timedelta

from queue import Queue

from crawler.config import crawler_config_mongo as crawler_config
from crawler.exc import SkipCrawler, TerminatedCrawler
from crawler.worker.clien import Clien
from crawler.worker.ppomppu import Ppomppu
from crawler.worker.ruliweb_hobby import RuliwebHobby
from crawler.worker.ruliweb_hotdeal import RuliwebHotdeal
from crawler.worker.ruliweb_humor import RuliwebHumor
from crawler.worker.slrclub import Slrclub
from crawler.worker.todayhumor import Todayhumor
from crawler.worker.slrclub_hot import Slrclub_Hot


logger = logging.getLogger('crawler')
logging.config.dictConfig(crawler_config.logging_formatter)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Crawler(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.is_stop = False
        self.queue = queue

    def run(self):
        l = logger.getChild('Crawler.run')
        site = self.queue.get()

        try:
            site.do()
        except SkipCrawler:
            l.info('Crawler Skip')
        except:
            l.error('Unhandled Exception')
        l.info('============Crawler done==============')
        self.queue.task_done()


def crawler(*, queue: Queue):
    sites = [
        Clien(threshold=20, page_max=10),
        Ppomppu(threshold=30, page_max=10),
        # Slrclub(threshold=30, page_max=10),
        Todayhumor(threshold=40, page_max=10),
        RuliwebHobby(threshold=35, page_max=5),
        RuliwebHumor(threshold=35, page_max=5),

        # Slrclub_Hot(threshold=40, page_max=7000),
        # RuliwebHotdeal(threshold=15, page_max=10),
    ]
    thread_num = len(sites)
    for site in sites:
        queue.put(site)
    workers = []
    for i in range(thread_num):
        t = Crawler(queue)
        t.daemon = True
        workers.append(t)
        t.start()
    return workers


if __name__=='__main__':
    l = logger.getChild('main')
    oldtime = datetime.now()
    l.info('crawler start')
    count = 0
    queue = Queue()
    try:
        interval = crawler_config.crawler_interval
        seed = timedelta(minutes=random.randint(
            int(interval['minutes_min']), int(interval['minutes_max'])),
            seconds=int(interval['sec']))

        workers = crawler(queue=queue)
        queue.join()
        count += 1
        l.info("finish crawler: {}".format(count))
    except (KeyboardInterrupt, TerminatedCrawler):
        l.info('terminated crawler')
        exit()
