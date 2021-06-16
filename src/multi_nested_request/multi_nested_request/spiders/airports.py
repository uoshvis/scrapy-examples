# working example https://stackoverflow.com/questions/41634126/multiple-nested-request-with-scrapy

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import CountryItem, AirportItem
from time import time
import json


class AirportsSpider(CrawlSpider):
    name = 'airports'
    allowed_domains = ['flightradar24.com']
    start_urls = ['https://www.flightradar24.com/data/airports']

    rules = (
        Rule(LinkExtractor(allow=r'data/airports'), callback='parse', follow=True),
    )

    def parse(self, response):
        count_country = 0
        countries = []
        # parse country
        for country in response.xpath('//a[@data-country]'):
            if count_country > 3:
                break
            item = CountryItem()
            url = country.xpath('./@href').get()
            name = country.xpath('./@title').get()
            item['link'] = url
            item['name'] = name
            count_country += 1
            countries.append(item)
            # parse country airports
            yield scrapy.Request(url, meta={'my_country_item': item}, callback=self.parse_airports)

    def parse_airports(self, response):
        item = response.meta['my_country_item']
        item['airports'] = []
        # parse country airports
        for airport in response.xpath('//a[@data-iata]'):
            url = airport.xpath('./@href').get()
            iata = airport.xpath('./@data-iata').get()
            iatabis = airport.xpath('./small/text()').get()
            name = ''.join(airport.xpath('./text()').get()).strip()
            lat = airport.xpath("./@data-lat").get()
            lon = airport.xpath("./@data-lon").get()

            iAirport = AirportItem()
            iAirport['name'] = name
            iAirport['link'] = url
            iAirport['lat'] = lat
            iAirport['lon'] = lon
            iAirport['code_little'] = iata
            iAirport['code_total'] = iatabis
            item['airports'].append(iAirport)

        urls = []
        for airport in item['airports']:
            json_url = 'https://api.flightradar24.com/common/v1/airport.json?code={code}&plugin[]=&plugin-setting[schedule][mode]=&plugin-setting[schedule][timestamp]={timestamp}&page=1&limit=50&token='.format(
                code=airport['code_little'], timestamp=int(time()))
            urls.append(json_url)
        if not urls:
            return item

        # start with first url
        next_url = urls.pop()
        return scrapy.Request(next_url, self.parse_schedule,
                              meta={'airport_item': item, 'airport_urls': urls, 'i': 0})

    def parse_schedule(self, response):
        # loop this continuously for every schedule item
        item = response.meta['airport_item']
        i = response.meta['i']
        urls = response.meta['airport_urls']
        json_load = json.loads(response.text)
        # item['airports'][i]['schedule'] = json_load['result']['response']['airport']['pluginData']['schedule']
        item['airports'][i]['schedule'] = 'schedule ' + str(i)
        if not urls:
            yield item
            return
        url = urls.pop()
        yield scrapy.Request(url, self.parse_schedule,
                             meta={'airport_item': item, 'airport_urls': urls, 'i': i + 1})
