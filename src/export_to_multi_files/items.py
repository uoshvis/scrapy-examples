# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AuthorItem(scrapy.Item):
    title = scrapy.Field()
    time = scrapy.Field()
    author = scrapy.Field()


class QuoteItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    quote = scrapy.Field()
