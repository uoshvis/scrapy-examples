import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Selector
from scrapy.loader import ItemLoader
from scrapy.item import Item, Field
from itemloaders.processors import Join, MapCompose


def strip_quote(value):
    return value.strip('“').strip('”')


class QuoteItem(Item):
    quote = Field()
    author = Field()
    link = Field()


class MySpider(scrapy.Spider):
    name = 'scraper_name'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    quotes_list_xpath = '//div[@class="quote"]'
    item_fields = {
        'quote': './span[@class="text"]/text()',
        'author': './span/small[@class="author"]/text()',
        'link': './span/a/@href'
    }

    def parse(self, response):
        selector = Selector(response)
        for quote in selector.xpath(self.quotes_list_xpath):
            loader = ItemLoader(item=QuoteItem(), selector=quote)
            loader.default_input_processor = MapCompose(strip_quote, str.strip)
            loader.default_output_processor = Join()
            for field, xpath in self.item_fields.items():
                loader.add_xpath(field, xpath)
            yield loader.load_item()


if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'CONCURRENT_REQUESTS': 2
    })
    process.crawl(MySpider)
    process.start()
