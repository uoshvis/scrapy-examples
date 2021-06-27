# Examples of spider settings

```
# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

ROBOTSTXT_OBEY = True
DEFAULT_REQUEST_HEADERS = {
   "Accept": "application/json, text/javascript, */*; q=0.01",
   "DNT": "1",
   "Accept-Encoding": "gzip, deflate, br",
   "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8",
   "x-requested-with": "XMLHttpRequest",
}

DOWNLOAD_DELAY = 5
```

**Real request header example**
https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending

**Download delay as spider attribute**
```
class MySpider(scrapy.Spider): 
    name = 'myspider' 
    download_delay = 5.0 
```