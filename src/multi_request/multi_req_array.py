# https://stackoverflow.com/questions/56486114/collect-items-from-multiple-requests-in-an-array-in-scrapy

'''
Another approach is to use a separate spider for all "grouped" requests.
You can start those spiders programmatically and pass a bucket (e.g. a dict) as spider attribute.
Within your pipeline you add your items from each request to this bucket.
From "outside" you listen to the spider_closed signal and get this bucket which then contains all your items.

Look here for how to start a spider programatically via a crawler runner:
https://docs.scrapy.org/en/latest/topics/practices.html#running-multiple-spiders-in-the-same-process

'''

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals


def on_spider_closed(spider, reason):
    bucket = spider.bucket
    print('Called bucket.. *********************')
    print('Spider ended: ', spider.name, reason)


class MySpider1(scrapy.Spider):
    name = 'foo'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        self.bucket['foo_url'] = response.url
        # yield dict(egg='hello_world')


class MySpider2(scrapy.Spider):
    name = 'bar'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        self.bucket['bar_url'] = response.url
        yield dict(bar='hello_world')


class MyPipeline(object):
    def process_item(self, item, spider):
        return item


if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'CONCURRENT_REQUESTS': 2,
        'ITEM_PIPELINES':  {'__main__.MyPipeline': 1}
    })
    process.crawl(MySpider1, bucket=dict())
    process.crawl(MySpider2, bucket=dict())
    dispatcher.connect(on_spider_closed, signal=scrapy.signals.spider_closed)
    process.start()


