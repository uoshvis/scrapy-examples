# working example
# https://stackoverflow.com/questions/25095233/correct-way-to-nest-item-data-in-scrapy/25096896#25096896
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from scrapy.selector import Selector
from time import time


class MetaItem(Item):
    url = Field()
    added_on = Field()


class MainItem(Item):
    price = Field()
    title = Field()
    meta = Field(serializer=MetaItem)


class MainItemLoader(ItemLoader):
    default_item_class = MainItem
    default_output_processor = TakeFirst()


class MetaItemLoader(ItemLoader):
    default_item_class = MetaItem
    default_output_processor = TakeFirst()


class MySpider(scrapy.Spider):
    name = 'scraper_name'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        main_loader = MainItemLoader(selector=Selector(response))
        main_loader.add_value('title', 'test')
        main_loader.add_value('price', 'price')
        main_loader.add_value('meta', self.get_meta(response))
        return main_loader.load_item()

    def get_meta(self, response):
        main_loader = MetaItemLoader(selector=Selector(response))
        main_loader.add_value('url', response.url)
        main_loader.add_value('added_on', int(time()))
        return main_loader.load_item()

    # Another version

    # def parse(self, response):
    #     item = MainItem()
    #     item['meta'] = {'added_on': int(time())}
    #     item['meta']['url'] = response.url
    #     return item


if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'CONCURRENT_REQUESTS': 2
    })
    process.crawl(MySpider)
    process.start()
