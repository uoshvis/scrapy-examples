# Workaround: Requests Stack
# Pass the list of subsequent requests around and provide the request with an errback
# to catch erroneous responses and continue execution
# This solution is still synchronous, and the requests are performed in the order of the call stack

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst


class Tag(Item):
    pos = Field()
    tag = Field()
    url = Field()
    quotes = Field()
    text = Field()
    author = Field()
    author_url = Field()
    second_url = Field()
    third_url = Field()


class MySpider(scrapy.Spider):
    name = 'scraper_name'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def call_next(self, response):
        '''
        Call next target for the item loader, or yields it if completed.
        Call the next request so long as the stack isn't empty.
        Yield the item once completed.
        The method is used as both the callback and errback of the request.
        The other part is an object callstack, which contains the request url, and the actual processing callback.
        It is passed to all requests via the meta attribute.
        Get the meta object
        response does not contain it.
        '''

        meta = response.request.meta
        # Items remaining in the stack? Execute them
        if len(meta['callstack']) > 0:
            target = meta['callstack'].pop(0)
            yield scrapy.Request(target['url'], meta=meta, callback=target['callback'], errback=self.call_next)
        else:
            yield meta['loader'].load_item()

    def parse(self, response):
        tags = response.xpath('//span[@class="tag-item"]/a')
        for i, tag in enumerate(tags):
            url = urljoin(response.url, tag.xpath('@href').get())
            tag_name = tag.xpath('text()').get()
            pos = i + 1
            l = ItemLoader(item=Tag(), response=response)
            l.default_output_processor = TakeFirst()
            l.add_value('pos', pos)
            l.add_value('url', url)
            l.add_value('tag', tag_name)
            yield scrapy.Request(url, meta={'loader': l}, callback=self.load_first)

    def load_first(self, response):
        # Recover item(loader)
        l = response.meta['loader']
        quotes = response.xpath('//div[@class="quote"]')
        for quote_selector in quotes:
            text = quote_selector.xpath('./span[@class="text"]/text()').get().strip('”').strip('“')
            author = quote_selector.xpath('./span/small[@class="author"]/text()').get()
            author_url = urljoin(response.url, quote_selector.xpath('./span/a/@href').get())
            tag_url = urljoin(response.url, quote_selector.xpath('./div/a[@class="tag"]/@href').get())
            l.add_value('text', text)
            l.add_value('author', author)
            l.add_value('author_url', author_url)

            # Build the call stack
            callstack = [
                {'url': author_url,
                 'callback': self.load_second},
                {'url': tag_url,
                 'callback': self.load_third}
            ]
            response.meta['callstack'] = callstack
            return self.call_next(response)

    def load_second(self, response):
        # Recover item(loader)
        l = response.meta['loader']
        # Use just as before
        l.add_value('second_url', response.url)

        return self.call_next(response)

    def load_third(self, response):
        l = response.meta['loader']
        l.add_value('third_url', response.url)
        return self.call_next(response)


if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'CONCURRENT_REQUESTS': 2,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'result.json',
    })
    process.crawl(MySpider)
    process.start()
