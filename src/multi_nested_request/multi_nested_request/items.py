# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CountryItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    airports = scrapy.Field()


class AirportItem(scrapy.Item):
    name = scrapy.Field()
    code_little = scrapy.Field()
    code_total = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    link = scrapy.Field()
    schedule = scrapy.Field()
