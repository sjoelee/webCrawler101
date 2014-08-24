from scrapy.contrib.spiders import CrawlSpider, Rule
#from scrapy.contrib.exporter import JsonItemExporter
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import Selector
from yellowPages.items import YellowpagesItem
from scrapy.http import Request

import json

class YellowPageSpider(CrawlSpider):
    name = "yellowpages"
    allowed_domains = ['www.yellowpages.com']
    businesses = []

#    start_urls = ['http://www.yellowpages.com/tucson-az/mip/cupcakes-456735205?lid=456735205']
    # start with one page
    start_urls = ['http://www.yellowpages.com/tucson-az/cupcakes?g=tucson%2C%20az&q=cupcakes']

    rules = (
        # Rule(SgmlLinkExtractor(allow=('\d+\?lid=\d+$',),),
        #           callback='parse_business_page', follow=True),
             Rule(SgmlLinkExtractor(allow=('relevance\&page=\d?$',),
                                    restrict_xpaths=('//*[@id="main-content"]/div[4]/div[5]/ul',)),
                  follow=True),
    )

    base_url = 'http://www.yellowpages.com'
    
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
            businessItem['Name']   = hxs.xpath(businessXPath + suffixBusinessName).extract()
            businessItem['Street'] = hxs.xpath(businessXPath + suffixBusinessStreet).extract()
            businessItem['Postal'] = hxs.xpath(businessXPath + suffixBusinessPostal).extract()
            businessItem['Phone']  = hxs.xpath(businessXPath + suffixBusinessPhone).extract()

            businesses.append(businessItem)

        return businesses
        
    # def parse(self, response):
    #     yield Request(response.url, callback = self.parse_business_listings_page)

    def parse_business_page(self, response):
        hxs = Selector(response)
        categories = hxs.xpath('//*[@id="business-details"]/dl/dd[4]')
        contact = hxs.xpath('//*[@id="main-content"]/div[1]/div[1]/div/section[2]/div[1]')
        businessItem = YellowpagesItem()
        bNameXPath_list = hxs.xpath('//*[@id="main-content"]/div[1]/div[1]/h1/text()').extract()        
        businessItem['Name'] = bNameXPath_list[0] if bNameXPath_list else ''
        bStreetXPath_list = contact.xpath('./p[@class="street-address"]/text()').extract()
        businessItem['Street'] = bStreetXPath_list[0] if bStreetXPath_list else ''
        bCityState_list = contact.xpath('./p[@class="city-state"]/text()').extract()
        businessItem['City_State'] = bCityState_list[0] if bCityState_list else ''
        bPhone_list = contact.xpath('./p[@class="phone"]/text()').extract()
        businessItem['Phone'] = bPhone_list[0] if bPhone_list else ''

        # print businessItem['Name']
        # print businessItem['Street']
        # print businessItem['City_State']
        # print businessItem['Phone']

        return businessItem

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

