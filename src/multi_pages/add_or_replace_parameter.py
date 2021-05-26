import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http.request import Request

from w3lib.url import add_or_replace_parameter
import json


class MySpider(scrapy.Spider):
    name = 'education'
    allowed_domains = ['data.un.org']
    start_urls = ['http://data.un.org/Data.aspx?d=UNESCO&f=series%3ANER_1']

    api_url = 'http://data.un.org/Handlers/DataHandler.ashx?Service=page&Page=3&DataFilter=series:NER_1&DataMartId=UNESCO'

    def parse(self, response):
        max_page = int(response.xpath('//*[@id="spanPageCountB"]/text()').re_first(r'\d+', '0'))
        for page in range(1, max_page + 1):
            yield Request(
                url=add_or_replace_parameter(self.api_url, 'Page', page),
                callback=self.parse_table)

    def parse_table(self, response):
        for tr in response.xpath('//table/tr'):
            item = dict()
            item['country'] = tr.xpath('./td[1]/text()').get()
            item['years'] = tr.xpath('./td[position()>1]/text()').getall()
            yield item

            with open('add_output.jsonl', 'a') as f:
                f.write(json.dumps(item, indent=4) + '\n')


if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'CONCURRENT_REQUESTS': 2
    })
    process.crawl(MySpider)
    process.start()
