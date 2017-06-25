# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['uk.farnell.com']
    start_urls = ['https://www.uk.farnell.com']

    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        #for url in self.start_urls:
        yield scrapy.Request(self.start_urls[0], headers=headers)

    # Will parse all first level categories
    def parse(self, response):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        results = response.css('li > a::attr(href)').extract()
        for url in results:
            if "http:" in url:
                continue
            else:
                if "/c/" in url:
                    yield scrapy.Request("".join((self.start_urls[0], url)), headers=headers, callback=self.parse1)

    # Will parse second level categories links
    def parse1(self, response):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        results = response.css('.filterCategoryLevelOne li > a::attr(href)').extract()
        #for url in results:

    def parseProductPage(self, response):

            #    yield scrapy.Request(url, headers=headers)
        #for el in response.css("li > a::attr(href)"):
            #print el
            # print el.extract_first()
            #next_page_url = response.css("li.next > a::attr(href)").extract_first()
            #yield scrapy.Request(response.urljoin(next_page_url))
            # yield {
            #     'text': el.css("::text").extract_first(),
            #     # 'author': quote.css("small.author::text").extract_first(),
            #     # 'tags': quote.css("div.tags > a.tag::text").extract()
            # }

        #next_page_url = response.css("li.next > a::attr(href)").extract_first()
        #if next_page_url is not None:
        #    yield scrapy.Request(response.urljoin(next_page_url))
