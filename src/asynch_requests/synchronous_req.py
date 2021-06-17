# Naive approach
# The requests are now synchronous, and the retrieval of the item now depends on all steps.
# If one request fails (for whatever reason), the item is lost

#  This solution fails often and some of my partially extracted items are lost

import scrapy
from scrapy.crawler import CrawlerProcess


class MySpider(scrapy.Spider):
    name = 'scraper_name'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        l = ItemLoader(item=MyCoolItem(), response=response)
        l.add_css('some_paragraphs', '.content > p')
        yield Request('example.org/foo/bar', meta={'loader': l}, callback=self.secondRequest)

    def secondRequest(self, response):
        # Recover ItemLoader
        l = response.meta['loader']
        l.add_css('other_stuff', '.foobar')

        # Complete the loader, yielding the completed item

        yield l.load_item()


if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'CONCURRENT_REQUESTS': 2
    })
    process.crawl(MySpider)
    process.start()
