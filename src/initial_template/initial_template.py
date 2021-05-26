import scrapy
from scrapy.crawler import CrawlerProcess


class MySpider(scrapy.Spider):
    name = 'scraper_name'
    start_urls = ['http://quotes.toscrape.com/']

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    def parse(self, response):
        yield dict(egg='hello_world')


if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()
