import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Selector


class MySpider(scrapy.Spider):
    name = 'scraper_name'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    text = """
    <ul>
        <li class="title"><h2>Monday</h2></li>
        <li>Item M1</li>
        <li>Item M2</li>
        <li>Item M3</li>
    </ul>
    <ul>
        <li class="title"><h2>Tuesday</h2></li>
        <li>Item T1</li>
        <li>Item T2</li>
        <li>Item T3</li>
    </ul>
    """

    def parse(self, response):
        sel = Selector(text=self.text)
        item = {}
        item['menu'] = {}
        uls = sel.xpath('//ul')
        # iterate over all uls
        for ul in uls:
            # extract the ul's li's
            lis = ul.xpath('li')
            # use the h2 text as the key and all the text from the remaining as values
            # with enumerate to add the alt logic
            item['menu'][lis[0].xpath('h2/text()').get()] = {"alt{}".format(i): node.xpath('text()').get() for i, node in enumerate(lis[1:], 1)}
            yield item


if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'CONCURRENT_REQUESTS': 2
    })
    process.crawl(MySpider)
    process.start()
