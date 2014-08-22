from scrapy.contrib.spiders import CrawlSpider, Rule
#from scrapy.contrib.exporter import JsonItemExporter
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import Selector
from yellowPages.items import YellowpagesItem
from scrapy.http import Request

import json

class YellowPageSpider(CrawlSpider):
    name = "yellowpages_v2.com"
    allowed_domains = ["www.yellowpages.com"]
    businesses = []
    # Note: need to make this flexible to user input
    # start with one page
    start_urls = [
        "http://www.yellowpages.com/tucson-az/cupcakes?g=tucson%2C%20az&q=cupcakes",
        ]
    base_url = "http://www.yellowpages.com"

# Need to implement rules that go to the business listing
    rules = (
#        Rule(LxmlLinkExtractor(allow=('//page=\d*',),
#                               restrict_xpaths=('//*[@id="main-content"]/div[4]/div[5]/ul',)),
#                               callback='parse_business_listings_page', follow=True),
        Rule(SgmlLinkExtractor(allow=('.*\d+\?lid=\d+$',),),
                               callback='parse_business_page', follow=True),
        )

    def extract_businesses_from_response(self,response):
        hxs = Selector(response)

        businessIDs = hxs.xpath('//*[@id="main-content"]/div[4]/div[3]/div/@id').extract()
        businesses = []

        for business in businessIDs:
            businessXPath = '//*[@id="'+business+'"]/div/div[2]/div[2]'
            suffixBusinessName    = '/h3/a[1]/span/text()'
            suffixBusinessStreet  = '/div/div[1]/p/span[1]/text()'
            suffixBusinessPostal  = '/div/div[1]/p/span[4]/text()'
            suffixBusinessPhone   = '/div/div[1]/ul/li/text()'

            businessItem = YellowpagesItem()
            businessItem['businessName']   = hxs.xpath(businessXPath + suffixBusinessName).extract()
            businessItem['businessStreet'] = hxs.xpath(businessXPath + suffixBusinessStreet).extract()
            businessItem['businessPostal'] = hxs.xpath(businessXPath + suffixBusinessPostal).extract()
            businessItem['businessPhone']  = hxs.xpath(businessXPath + suffixBusinessPhone).extract()

            businesses.append(businessItem)

        return businesses
        
    def parse(self, response):
        yield Request(response.url, callback = self.parse_business_listings_page)

    def parse_business_page(self, response):
        print "Visiting business listing %s" % response.url

    def parse_business_listings_page(self, response):
        print "Visiting %s" % response.url

        self.businesses.append(self.extract_businesses_from_response(response))
        hxs = Selector(response)
        li_tags = hxs.xpath('//*[@id="main-content"]/div[4]/div[5]/ul/li')
        next_exist = False
        
        # Check to see if there's a "Next". If there is, store the links.
        # If not, return. 
        # This requires a linear search through the list of li_tags. Is there a faster way?
        for li in li_tags:
            li_text = li.xpath('.//a/text()').extract()
            li_data_page = li.xpath('.//a/@data-page').extract()
            # Note: sometimes li_text is an empty list so check to see if it is nonempty first
            if (li_text and li_text[0] == 'Next'):
                next_exist = True
                next_page_num = li_data_page[0]

        if next_exist:
            for li in li_tags:
                li_text = li.xpath('.//a/text()').extract()
                li_href = li.xpath('.//a/@href').extract()
                li_data_page = li.xpath('.//a/@data-page').extract()
                if (li_data_page and li_data_page[0] == next_page_num and li_href):
                    url = self.base_url + li_href[0]
                    yield Request(url, callback=self.parse_business_listings_page)

