import scrapy
from scrapy.crawler import CrawlerProcess


class AustmpsItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    district = scrapy.Field()
    link = scrapy.Field()
    twitter = scrapy.Field()
    party = scrapy.Field()
    phonenumber = scrapy.Field()


class MySpider(scrapy.Spider):
    name = 'austmpdata'
    allowed_domains = ['www.aph.gov.au']
    start_urls = ['https://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?q=&mem=1&par=-1&gen=0&ps=0']

    def parse(self, response):
        # The main method of the spider. It scrapes the URL(s) specified in the
        # 'start_url' argument above. The content of the scraped URL is passed on
        # as the 'response' object.
        next_page_url = response.xpath("//a[@title='Next page']/@href")

        if next_page_url:
            path = next_page_url.get()
            next_page = response.urljoin(path)
            print("Found url: {}".format(next_page))  # Write a debug statement
            yield scrapy.Request(next_page, callback=self.parse)  # Return a call to the function "parse"

        # When asked for a new item, ask self.scrape for new items and pass them along
        yield from self.scrape(response)

    def scrape(self, response):
        for resource in response.xpath("//h4[@class='title']/.."):
            # Loop over each item on the page.
            item = AustmpsItem()

            item['name'] = resource.xpath("h4/a/text()").get()
            profile_page = response.urljoin(resource.xpath("h4/a/@href").get())
            item['link'] = profile_page
            item['district'] = resource.xpath("dl/dd/text()").get()
            item['twitter'] = resource.xpath("dl/dd/a[contains(@class, 'twitter')]/@href").get()
            item['party'] = resource.xpath("dl/dt[text()='Party']/following-sibling::dd/text()").get()
            # We need to make a new variable that the scraper will return that will get passed through another callback.
            # We're calling that variable "request"

            request = scrapy.Request(profile_page, callback=self.get_phonenumber)
            request.meta['item'] = item
            yield request

    def get_phonenumber(self, response):
        # A scraper designed to operate on one of the profile pages
        item = response.meta['item']  # Get the item we passed from scrape()
        item['phonenumber'] = response.xpath(
            "//h3[text()='Electorate Office ']/following-sibling::dl/dd[1]/a/text()").extract_first()
        yield item  # Return the new phonenumber'd item back to scrape


if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'CONCURRENT_REQUESTS': 2,
        'DEPTH_LIMIT': 1
    })
    process.crawl(MySpider)
    process.start()

# $ rm output.csv
# $ scrapy crawl austmpdata -o output.csv
# $ wc -l output.csv