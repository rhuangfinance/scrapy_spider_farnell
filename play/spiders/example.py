# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['uk.farnell.com']
    start_urls = ['https://www.uk.farnell.com']

    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        yield scrapy.Request(self.start_urls[0], headers=headers)

    # Will parse all first level categories
    def parse(self, response):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        results = response.css('li > a::attr(href)').extract()
        for url in results:
            if not "http:" in url and "/c/" in url:
                yield scrapy.Request("".join((self.start_urls[0], url)), headers=headers, callback=self.parse1)

    # Will parse second level categories links
    def parse1(self, response):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        #results = response.css('.filterCategoryLevelOne li > a::attr(href)').extract()
        labels = response.css('.filterCategoryLevelOne li > a::text').extract()
        for lab in labels:
            print lab

    def parseProductPage(self, response):
        pass
