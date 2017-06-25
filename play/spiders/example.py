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
        'http://uk.farnell.com/wurth-elektronik/7488920245/chip-antenna-multilayer-2-4-2/dp/2425052',
        'http://uk.farnell.com/hirschmann-testmeasurement/931667100/test-plug-black-buela/dp/1011412'
    ]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[4], headers=self.headers)

    # Parser for components results
    def parse(self, response):
        productDetails = {
            'url': None,
            'brand': None,
            'title': None,
            'unit_price': None,
            'content': None,
            'information': None
        }
        productDetails['url'] = response.css('div#breadcrumb > ul > li > a.omTagEvt::attr(href)')[-1].extract()
        productDetails['brand'] = response.css('span.schemaOrg::text').extract_first()
        productDetails['title'] = '-'.join((productDetails['brand'], response.css('div#breadcrumb > ul > li > a.omTagEvt::text')[-1].extract()))
        unit_price = response.css('span.price::text').extract_first().strip().replace('','')[1:] # removing currency character
        productDetails['unit_price'] = float(unit_price)
        productDetails['content'] = response.css('div.contents::text').extract_first()
        information_name_dict = response.css('section.pdpProductContent > div.collapsable-content > dl > dt > label::text').extract()
        information_value_dict = response.css('section.pdpProductContent > div.collapsable-content > dl > dd > a::text').extract()
        dict_info = []
        cpt_info = 0
        for key in information_name_dict:
            dict_info.append({
                'name': key,
                'value': information_value_dict[cpt_info]
            })
            cpt_info = cpt_info+1
        productDetails['information'] = dict_info
        productDetails['manufacturer'] = productDetails['brand']
        productDetails['manufacturer_part'] = str(response.xpath('//dd[@itemprop="mpn"]//text()').extract_first().split()[0])
        productDetails['tariff_number'] = response.xpath('//*[@id="pdpSection_ProductLegislation"]/div[2]/dl/dd[3]/text()').extract_first().split()[0]
        productDetails['origin_country'] = response.xpath('//*[@id="pdpSection_ProductLegislation"]/div[2]/dl/dd[1]/text()').extract_first().split()[0]

        #
        # //*[@id="pdpSection_ProductLegislation"]/div[2]/dl/dt[4]
        # for scope in response.xpath('//div[@itemscope]'):
        #     print "current scope:", scope.xpath('@itemtype').extract()
        #     props = scope.xpath('''set:difference(./descendant::*/@itemprop,
        #         .//*[@itemscope]/*/@itemprop)''')
        #     print "properties:", props.extract()
        # mpn = response.xpath('//meta[@itemprop="mpn"]/@content').extract()
        # print mpn
        # mpn = response.xpath('//div[@itemprop=`mpn`]//text()').extract_first()
        # productDetails['manufacturer_part'] = response.xpath('//div[@itemprop=mpn]//text()').extract_first()

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
