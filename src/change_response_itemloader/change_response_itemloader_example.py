def parse(self, response):

    l = ItemLoader(item=YourItem(), response=response)
    l.add_xpath('Field1', '...')
    l.add_value('Field2', '...')

    item = l.load_item()

    yield scrapy.Request(
        url=another_url,
        callback=self.second,
        meta={'item': item}
    )

def second(self, response):

    l = ItemLoader(item=response.meta["item"], response=response)
    l.add_xpath("Field3", '...')

    yield l.load_item()