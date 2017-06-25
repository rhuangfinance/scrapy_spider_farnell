# -*- coding: utf-8 -*-
import scrapy
from os.path import basename

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['uk.farnell.com']
    headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
    start_urls = [
        'http://www.uk.farnell.com',
        'http://uk.farnell.com/c/passive-components/resistors-fixed-value/chip-smd-resistors',
        'http://uk.farnell.com/c/passive-components/antennas-single-band-chip',
        'http://uk.farnell.com/wurth-elektronik/7488920245/chip-antenna-multilayer-2-4-2/dp/2425052',
        'http://uk.farnell.com/hirschmann-testmeasurement/931667100/test-plug-black-buela/dp/1011412',
        'http://uk.farnell.com/molex/43030-0009/contact-socket-24-20-awg-crimp/dp/2101965'
    ]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], headers=self.headers)

    # Will parse all first level categories
    def parse(self, response):
        results = response.css('li > a::attr(href)').extract()
        for url in results:
            if not "http:" in url and "/c/" in url:
                yield scrapy.Request("".join((self.start_urls[0], url)), headers=self.headers, callback=self.parse1)

    # Will parse second level categories links
    def parse1(self, response):
        categories = response.css('.filterCategoryLevelOne li > a::attr(href)').extract()
        for url in categories:
            if "http:" in url:
                yield scrapy.Request(url, headers=self.headers, callback=self.parse2)

    # Will parse the results table composed of products
    def parse2(self, response):
        products = response.css('table#sProdList > tbody > tr > td.mftrPart > a::attr(href)').extract()
        for url in products:
            if "http:" in url:
                yield scrapy.Request(url, headers=self.headers, callback=self.parseProductPage)

        # Go to next page if any
        next_page_url = response.css("div.paginNext.pageLink  > a.nextLinkPara ::attr(href)").extract_first()
        if next_page_url != None:
            yield scrapy.Request(next_page_url, headers=self.headers, callback=self.parse2)

    def parseProductPage(self, response):
        productDetails = {
            'url': None,
            'brand': None,
            'title': None,
            'unit_price': None,
            'content': None,
            'information': None,
            'manufacturer': None,
            'manufacturer_part': None,
            'tariff_number': None,
            'origin_country': None,
            'file_urls': None,
            'files': None,
            'primary_image_url': None,
            'image_urls': None,
            'trail': None
        }
        productDetails['url'] = response.css('div#breadcrumb > ul > li > a.omTagEvt::attr(href)')[-1].extract()
        productDetails['brand'] = response.css('span.schemaOrg::text').extract_first()
        productDetails['title'] = '-'.join((productDetails['brand'], response.css('div#breadcrumb > ul > li > a.omTagEvt::text')[-1].extract()))
        unit_price = response.css('span.price::text').extract_first()
        if unit_price != None:
            unit_price = unit_price.replace(',', '')
            unit_price = float(unit_price.strip()[1:]) # removing currency character
        productDetails['unit_price'] = unit_price
        productDetails['content'] = response.css('div.contents::text').extract_first()
        information_name_dict = response.css('section.pdpProductContent > div.collapsable-content > dl > dt > label::text').extract()
        information_value_dict = response.css('section.pdpProductContent > div.collapsable-content > dl > dd > a::text').extract()
        dict_info = []
        cpt_info = 0
        for key in information_name_dict:
            dict_info.append({
                'name': key,
                'value': information_value_dict[cpt_info] if information_value_dict[cpt_info:] else None
            })
            cpt_info = cpt_info+1
        productDetails['information'] = dict_info
        productDetails['manufacturer'] = productDetails['brand']
        manufacturer_part = response.xpath('//dd[@itemprop="mpn"]//text()').extract_first()
        if manufacturer_part != None:
            manufacturer_part = str(manufacturer_part.split()[0])
        productDetails['manufacturer_part'] = manufacturer_part
        tariff_number = response.xpath('//*[@id="pdpSection_ProductLegislation"]/div[2]/dl/dd[3]/text()').extract_first()
        if tariff_number != None:
            tariff_number = tariff_number.split()[0]
        productDetails['tariff_number'] = tariff_number

        productDetails['origin_country'] = response.xpath('//*[@id="pdpSection_ProductLegislation"]/div[2]/dl/dd[1]/text()').extract_first().split()[0]
        productDetails['file_urls'] = response.xpath('//*[@id="technicalData"]/li/a/@href').extract()
        files = []
        for file_url in productDetails['file_urls']:
            files.append(basename(file_url))
        productDetails['files'] = files
        productDetails['primary_image_url'] = response.xpath('//img[@id="productMainImage"]/@src').extract_first()
        image_urls = []
        for image in response.xpath('//img/@src').extract():
            if '.jpg' in image:
                image_urls.append(image)
        productDetails['image_urls'] = image_urls
        productDetails['trail'] = response.css('div#breadcrumb > ul > li > a.omTagEvt::text').extract()
        print productDetails
