# Pseudo example code
import scrapy
from scrapy.crawler import CrawlerProcess


class MySpider(scrapy.Spider):
    name = 'scraper_name'
    allowed_domains = ['quotes.toscrape.com']

    def __init__(self):
        super(MySpider, self).__init__()
        self.start_urls = ['url_city_1', 'url_city_2']
        # Trackers
        self.page = 0
        self.object = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.page += 1
        self.logger.info(f'Search page N° {self.page}')
        # Getting the hotels list
        hotel_links = response.css('hotel_selector')

        # Following hotels pages
        for hotel in hotel_links:
            link = hotel.get('link')
            yield response.follow(url=link, callback=self.parse_hotel)

        # Get Next Page of hotels
        next_page = response.css('next_page_selector').extract()
        yield scrapy.Request(url=next_page.url, callback=self.parse)

    def parse_hotel(self, response):
        self.object += 1
        self.logger.debug(f'Hotel N° {self.object}')
        # Get hotel informations
        info_1 = response.css('info_1_selector')
        info_2 = response.css('info_2_selector')
        # ...

        yield {
            "info_1": info_1,
            "info_2": info_2
        }


if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'CONCURRENT_REQUESTS': 2
    })
    process.crawl(MySpider)
    process.start()
