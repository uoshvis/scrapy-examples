# Basic spider vs Crawler spider 

This example demonstrates differences between Basic spider and Crawler spider.

## Basic spider example
```
scrapy genspider -t basic weather_spider weather.com
```
Filename: weather_spider.py

To control the making of the requests use start_requests() instead of start_urls.

```
scrapy crawl weather_spider -o output.json
```

## Crawler spider example

```
scrapy genspider -t crawl crawl_spider books.toscrape.com
```
Filename crawl_spider.py

 Callback is not in the initial request because rules have the callback specified in it along with the URL using which subsequent requests are to be made.
 The crawling spider starts generating requests with all the URLs that the LinkExtractor has created with parse_books as the callback function.
 
```
scrapy crawl crawl_spider -o crawl_spider_output.json
```

**Rules replaced with parse_pages()**
```
scrapy genspider -t basic book_spider books.toscrape.com
```
Filename: book_spider.py

Rules replaced in crawling spider with a dedicated and long function parse_pages() in the basic spider.