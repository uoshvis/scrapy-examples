# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CountryItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    airports = scrapy.Field()
    other_url= scrapy.Field()
    last_updated = scrapy.Field(serializer=str)
