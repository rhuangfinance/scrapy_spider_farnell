# -*- coding: utf-8 -*-
import scrapy

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['uk.farnell.com']
    headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
    start_urls = [
        'https://www.uk.farnell.com',
        'http://uk.farnell.com/c/passive-components/resistors-fixed-value/chip-smd-resistors',
        'http://uk.farnell.com/c/passive-components/antennas-single-band-chip',
        'http://uk.farnell.com/wurth-elektronik/7488920245/chip-antenna-multilayer-2-4-2/dp/2425052'
    ]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[3], headers=self.headers)

    # Parser for components results
    def parse(self, response):
        productDetails = {}
        productDetails['url'] = response.css('div#breadcrumb > ul > li > a.omTagEvt::attr(href)')[-1].extract()
        print productDetails

    def start_requests0(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        yield scrapy.Request(self.start_urls[0], headers=self.headers)

    # Will parse all first level categories
    def parse0(self, response):
        results = response.css('li > a::attr(href)').extract()
        for url in results:
            if not "http:" in url and "/c/" in url:
                yield scrapy.Request("".join((self.start_urls[0], url)), headers=self.headers, callback=self.parse1)

    # Will parse second level categories links
    def parse1(self, response):
        categories = response.css('.filterCategoryLevelOne li > a::text').extract()
        for url in categories:
            if "http:" in url:
                yield scrapy.Request(url, headers=self.headers, callback=self.parse2)

    # Will parse the results table composed of products
    def parse2(self, response):
        products = response.css('table#sProdList > tbody > tr > td.mftrPart > a::attr(href)').extract()
        for url in products:
            if not "http:" in url:
                yield scrapy.Request(url, headers=self.headers, callback=self.parseProductPage)

    def parseProductPage(self, response):
        pass
