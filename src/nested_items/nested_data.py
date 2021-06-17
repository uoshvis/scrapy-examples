# Adapted example:
# https://dogsnog.blog/2019/03/16/how-to-produce-a-json-tree-with-nested-data-from-scrapy/

# Output structure see output.json

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
from urllib.parse import urljoin
from scrapy import signals
import json
import jsons


class TopTenTags(Item):
    tags = Field()


class Tag(Item):
    pos = Field()
    tag = Field()
    url = Field()
    quotes = Field()


class Quote(Item):
    text = Field()
    author = Field()


class MySpider(scrapy.Spider):
    name = 'scraper_name'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def __init__(self):
        super().__init__()
        # A flag, set after post-processing is finished, to avoid an infinite loop
        self.data_submitted = False
        # The object to return for conversion to a JSON tree.
        # All the parse methods add their results to this structure.
        self.top_tags = TopTenTags(tags=[])

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """Register to receive the idle event"""
        spider = super(MySpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    def spider_idle(self, spider):
        """Schedule a simple request in order to return the collected data"""
        if self.data_submitted:
            return

        # This is a hack: I don't yet know how to schedule a request to just
        # submit data _without_ also triggering a scrape. So I provide a URL
        # to a simple site that we're going to ignore.
        null_request = scrapy.Request('http://neverssl.com/', callback=self.submit_data)
        self.crawler.engine.schedule(null_request, spider)
        raise scrapy.exceptions.DontCloseSpider

    def submit_data(self, _):
        """Simply return the collection of all the scraped data. Ignore the actual
        scraped content. I haven't figured out another way to submit the merged
        results.
        To be used as a callback when the spider is idle (i.e., has finished scraping.)
        """
        self.data_submitted = True
        # convert obj to dict
        top_tags_dict = jsons.dump(self.top_tags)
        # write to json output
        with open('output.json', 'w') as f:
            json.dump(top_tags_dict, f, sort_keys=True, indent=4)
        return self.top_tags

    # Top-level parse method returns its data by creating an Item and adding it directly into the structure.
    # Finally, it yields the new Item to the next page’s parser
    def parse(self, response):
        # Create a new Category to hold the scraped info. Also,
        # prepare it for holding its brands.
        tags = response.xpath('//span[@class="tag-item"]/a')
        for i, tag in enumerate(tags):
            url = urljoin(response.url, tag.xpath('@href').get())
            tag_name = tag.xpath('text()').get()
            pos = i + 1
            tag = Tag(pos=pos, tag=tag_name, url=url, quotes=[])
            # Save the category into the tree structure.
            self.top_tags['tags'].append(tag)
            # Create a request for the Category's page, which
            # will list all its Brands.
            # Pass the Category Item in the meta dict.
            request = scrapy.Request(tag['url'], callback=self.parse_tag_page)
            request.meta['tag'] = tag
            yield request

    # In the parse method for the “next level down”, I do the same thing.
    # Except now, I save the newly created Item in the passed-in Category:
    def parse_tag_page(self, response):
        # Pull the category back out of the meta dict.
        parent_category = response.meta['tag']
        quotes = response.xpath('//div[@class="quote"]')
        for quote_selector in quotes:
            text = quote_selector.xpath('./span[@class="text"]/text()').get().strip('”').strip('“')
            author = quote_selector.xpath('./span/small[@class="author"]/text()').get()
            quote = Quote(text=text, author=author)
            parent_category['quotes'].append(quote)


if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'CONCURRENT_REQUESTS': 8
    })
    process.crawl(MySpider)
    process.start()

# Schedules a scrape just so that it can return data. It ignores the actual scrape results
# To get a proper JSON instance (with a hash at the top level), use the JSON Lines Feed Exporter.
