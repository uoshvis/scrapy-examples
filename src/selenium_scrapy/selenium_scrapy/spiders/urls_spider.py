import scrapy
from selenium import webdriver
import selenium.common.exceptions as exception

from logzero import logfile, logger
import time
import json


class UrlsSpiderSpider(scrapy.Spider):
    logfile("openaq_spider.log", maxBytes=1e6, backupCount=3)
    name = 'urls_spider'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://toscrape.com/']

    def start_requests(self):
        url = "http://quotes.toscrape.com"
        yield scrapy.Request(url=url, callback=self.parse_urls)

    def parse_urls(self, response):
        # Use headless option to not open a new browser window
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
        # Load the countries list written by countries_spider.py
        with open("countries_list.json", "r") as f:
            temp_list = json.load(f)
        countries_list = list(map(lambda x: x["country"], temp_list))
        total_url_count = 0
        for i, country in enumerate(countries_list):
            # Opening locations webpage
            driver.get("https://openaq.org/#/locations")
            driver.implicitly_wait(5)
            country_url_count = 0
            # Identifying country and clicking country checkboxes
            but = driver.find_element_by_xpath("//span[contains(text(),'Country')]")
            but.click()
            country_button = driver.find_element_by_xpath("//*[contains(text(), '" + country+"')]/parent::div")
            country_button.click()
            time.sleep(2)
            # Identifying country and clicking PM2.5 checkboxes
            but_par = driver.find_element_by_xpath("//span[contains(text(),'Parameter')]")
            but_par.click()
            values_button = driver.find_element_by_xpath("//span[contains(text(),'PM2.5')]/parent::label")
            values_button.click()
            time.sleep(2)

            while True:
                # Identifying locations from a subpage
                locations = driver.find_elements_by_xpath("//a[@class='cfa-go']")
                # Extracting URLs of locations from a subpage
                for loc in locations:
                    link = loc.get_attribute("href")
                    country_url_count += 1
                    yield {
                        "url": link,
                        "country": country
                    }
                # Pressing 'NEXT' button to navigate to next subpage
                try:
                    next_button = driver.find_element_by_xpath("//li[@class='next']")
                    next_button.click()
                except exception.NoSuchElementException:
                    logger.debug(f"Last page reached for {country}")
                    break

            logger.info(f"{country} has {country_url_count} PM2.5 URLs")
            total_url_count += country_url_count

        logger.info(f"Total PM2.5 URLs: {total_url_count}")
        driver.quit()
