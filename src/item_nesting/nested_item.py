import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field


class FamilyItem(Item):
    name = Field()
    sons = Field()


class SonsItem(Item):
    name = Field()
    grandsons = Field()


class GrandsonsItem(Item):
    name = Field()
    age = Field()
    weight = Field()


class MySpider(scrapy.Spider):
    name = 'scraper_name'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        gs1 = GrandsonsItem()
        gs1['name'] = 'GS1'
        gs1['age'] = 18
        gs1['weight'] = 50

        gs2 = GrandsonsItem()
        gs2['name'] = 'GS2'
        gs2['age'] = 19
        gs2['weight'] = 51

        s1 = SonsItem()
        s1['name'] = 'S1'
        s1['grandsons'] = [dict(gs1), dict(gs2)]

        jenny = FamilyItem()
        jenny['name'] = 'Jenny'
        jenny['sons'] = [dict(s1)]

        yield jenny

        # Output example

        # {'name': 'Jenny',
        #  'sons': [{'grandsons': [{'age': 18, 'name': 'GS1', 'weight': 50},
        #                          {'age': 19, 'name': 'GS2', 'weight': 51}],
        #            'name': 'S1'}]}


if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'CONCURRENT_REQUESTS': 1
    })
    process.crawl(MySpider)
    process.start()
