# working example https://stackoverflow.com/questions/41634126/multiple-nested-request-with-scrapy

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import CountryItem

class AirportsSpider(CrawlSpider):
    name = 'airports'
    allowed_domains = ['flightradar24.com']
    start_urls = ['https://www.flightradar24.com/data/airports']

    rules = (
        Rule(LinkExtractor(allow=r'data/airports'), callback='parse', follow=True),
    )

    def parse(self, response):
        count_country = 0
        countries = []
        for country in response.xpath('//a[@data-country]'):
            if count_country > 3:
                break
            item = CountryItem()
            url = country.xpath('./@href').get()
            name = country.xpath('./@title').get()
            item['link'] = url[0]
            item['name'] = name[0]
            count_country += 1
            countries.append(item)
            yield scrapy.Request(url[0], meta={'my_country_item': item}, callback=self.parse_airports)



    def parse_airports(self, response):
        pass