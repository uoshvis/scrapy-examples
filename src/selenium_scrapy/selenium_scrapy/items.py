import scrapy


class OpenaqItem(scrapy.Item):
    country = scrapy.Field()
    city = scrapy.Field()
    location = scrapy.Field()
    pm25 = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()