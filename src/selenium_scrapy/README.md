## Selenium integration with Scrapy

A web scraping example written in Python to demonstrate web scraping combining Selenium with Scrapy.
To run the project, Scrapy, Selenium and a webdriver needs to be installed.

On linux:
```
pip install Scrapy
pip install selenium
```
Webdriver for 5 major browsers are supported by Selenium. Chromedriver for Chrome browser can be installed using the following commands.

```
wget https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip

unzip chromedriver_linux64.zip

sudo mv chromedriver /usr/local/bin/
```
Geckodriver for Firefox can be installed with the following command.

`sudo apt install firefox-geckodriver`

**Alternative method**

chromedriver inside project location
```
import os
basedir = os.path.dirname(os.path.realpath('__file__'))
chrome_driver_path = os.path.join(basedir, 'chromedriver')
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options, executable_path=self.chrome_driver_path)
```
### Skeleton for combining Selenium with Scrapy
```
from scrapy import Selector
# Other Selenium and Scrapy imports
...
driver = webdriver.Chrome()
# Selenium tasks and actions to render the webpage with required content
selenium_response_text = driver.page_source
new_selector = Selector(text=selenium_response_text)
# Scrapy tasks to extract data from Selector
```

####Code execution
`countries_spider` extracts country names and stores it in a JSON file.
```
scrapy crawl countries_spider -o countries_list.json
```

`urls_spider` filters out countries and PM2.5 data using checkboxes

```
scrapy crawl urls_spider -o urls.json
```

`pm_data_scraper ` crawls all the URLs extracted by the above spider and extracts PM2.5

```
scrapy crawl pm_data_spider -o outpout.json
```

###Scrapy vs Selenium

Comparison code in `scrapy_VS_selenium.py` is available.
# Other integrations

`scrapy-splash` https://github.com/scrapy-plugins/scrapy-splash

`scrapy-selenium` https://github.com/clemfromspace/scrapy-selenium

## LOGGING with logzero

```
from logzero import logger, logfile
import time

# Initializing log file

logfile("openaq_spider.log", maxBytes=1e6, backupCount=3)
logger.info(f"Scraping started at {time.strftime('%H:%M:%S')}")

try:
    # try logic
    no_pm += 1

except Exception as e:
    logger.error(f"Exception {e} has occured with URL: {url}")
    exception_count += 1
except exceptions as f:
    logger.error(f"Selenium Exception {f} has occured with URL: {url}")
    exception_count += 1

logger.info("Chromedriver restarted")
logger.info(f"Scraping ended at {time.strftime('%H:%M:%S')}")
logger.info(f"Scraped {count} PM2.5 readings.")
logger.info(f"No PM2.5 values: {no_pm} & No. of IndexError: {exception_count}")

```
