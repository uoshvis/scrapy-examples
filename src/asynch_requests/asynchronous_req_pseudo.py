# Workaround: Requests Stack
# Pass the list of subsequent requests around and provide the request with an errback
# to catch erroneous responses and continue execution
# This solution is still synchronous, and the requests are performed in the order of the call stack

import scrapy
from scrapy.crawler import CrawlerProcess


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
            yield Request(target['url'], meta=meta, callback=target['callback'], errback=self.call_next)
        else:
            yield meta['loader'].load_item()

    def parse(self, response):
        l = ItemLoader(item=MyCoolItem(), response=response)
        l.add_css('some_paragraphs', '.content > p')
        yield Request('example.org/foo/bar', meta={'loader': l}, callback=self.secondRequest)

    def load_first(self, response):
        # Recover item(loader)
        l = response.meta['loader']

        # Use just as before
        l.add_css(...)

        # Build the call stack
        callstack = [
            {'url': '<some_url>',
             'callback': self.load_second},
            {'url': '<some_url>',
             'callback': self.load_third}
        ]

        return self.callnext(response)

    def load_second(self, response):
        # Recover item(loader)
        l = response.meta['loader']

        # Use just as before
        l.add_css(...)

        return self.callnext(response)

    def load_third(self, response):
        # ...

        return self.callnext(response)


if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'CONCURRENT_REQUESTS': 2
    })
    process.crawl(MySpider)
    process.start()
