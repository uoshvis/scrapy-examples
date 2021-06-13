# https://stackoverflow.com/questions/51088221/scrapy-export-parsed-data-into-multiple-files
import scrapy
from scrapy.loader import ItemLoader
from ..items import AuthorItem, QuoteItem
from itemloaders.processors import TakeFirst
from datetime import datetime


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quote_blocks = response.xpath('//div[@class="quote"]')
        for quote_block in quote_blocks:
            author_loader = ItemLoader(
                item=AuthorItem(),
                response=response,
                selector=quote_block)
            author_loader.default_output_processor = TakeFirst()
            author_loader.add_value('title', 'author')

            author_loader.add_value('time', datetime.now())
            author_loader.add_xpath('author', './/small[@class="author"]/text()')
            yield author_loader.load_item()

            quote_loader = ItemLoader(
                item=QuoteItem(),
                response=response,
                selector=quote_block)
            quote_loader.default_output_processor = TakeFirst()
            quote_loader.add_value('title', 'quote')
            quote_loader.add_value('url', response.url)
            quote_loader.add_xpath('quote', './/span[@class="text"]/text()')
            yield quote_loader.load_item()
