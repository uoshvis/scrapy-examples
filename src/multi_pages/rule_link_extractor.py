"""
Scrape multi pages
Using Rule with LinkExtractor
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class MySpider(CrawlSpider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    rules = (
        # Extract links matching xpath and parse them with the spider's method parse_table
        Rule(LinkExtractor(allow=(),
                           restrict_xpaths=('//li[@class="next"]',)),
             callback='parse_quote', follow=True),
    )

    def parse_quote(self, response):
        breakpoint()
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = dict()
        item['url'] = response.url
        return item


if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'CONCURRENT_REQUESTS': 2
    })
    process.crawl(MySpider)
    process.start()
