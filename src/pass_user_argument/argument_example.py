class MySpider(Spider):
    name = 'myspider'

    def parse(self, response):

        if self.parameter1 == value1:
            # this is True
            pass

        # or also
        if getattr(self, parameter2) == value2:
            # this is also True
            pass


# scrapy crawl myspider -a parameter1=value1 -a parameter2=value2