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
    count = 0
    num_request = 0

    start_urls = ['http://www.yellowpages.com/tucson-az/cupcakes?g=tucson%2C%20az&q=cupcakes']

    rules = (
             Rule(SgmlLinkExtractor(allow=('&page=\d$',),),#allow=('/tucson-az/cupcakes\?g=tucson%2C%20az&q=cupcakes&s=relevance&page=\d',),),
#                                    restrict_xpaths=('//*[@id="main-content"]/div[4]/div[5]/ul',)),
                  callback='parse_listings', follow=True),
             Rule(SgmlLinkExtractor(allow=('\d+\?lid=\d+$',),),
                  callback='parse_business_page', follow=True, process_request='parse_business_request'),
    )

    base_url = 'http://www.yellowpages.com'
    
    def parse_listings(self, response):
        print "Visiting %s" % response.url
        yield Request(response.url)

    def parse_business_request(self, request):
        self.num_request = self.num_request + 1
        print "# %d request sent to %s" % (self.num_request, request.url)

    def parse_business_page(self, response):
        hxs = Selector(response)
        categories = hxs.xpath('//*[@id="business-details"]/dl/dd[4]')
        contact = hxs.xpath('//*[@id="main-content"]/div[1]/div[1]/div/section[2]/div[1]')
        bNameXPath_list = hxs.xpath('//*[@id="main-content"]/div[1]/div[1]/h1/text()').extract()        
        bStreetXPath_list = contact.xpath('./p[@class="street-address"]/text()').extract()
        bCityState_list = contact.xpath('./p[@class="city-state"]/text()').extract()
        bPhone_list = contact.xpath('./p[@class="phone"]/text()').extract()

        businessItem = YellowpagesItem()
        businessItem['Name'] = bNameXPath_list[0] if bNameXPath_list else ''
        businessItem['Street'] = bStreetXPath_list[0] if bStreetXPath_list else ''
        businessItem['City_State'] = bCityState_list[0] if bCityState_list else ''
        businessItem['Phone'] = bPhone_list[0] if bPhone_list else ''

        self.count = self.count + 1
        print self.count

#        return businessItem

    # def extract_businesses_from_response(self,response):
    #     hxs = Selector(response)

    #     businessIDs = hxs.xpath('//*[@id="main-content"]/div[4]/div[3]/div/@id').extract()
    #     businesses = []

    #     for business in businessIDs:
    #         businessXPath = '//*[@id="'+business+'"]/div/div[2]/div[2]'
    #         suffixBusinessName    = '/h3/a[1]/span/text()'
    #         suffixBusinessStreet  = '/div/div[1]/p/span[1]/text()'
    #         suffixBusinessPostal  = '/div/div[1]/p/span[4]/text()'
    #         suffixBusinessPhone   = '/div/div[1]/ul/li/text()'

    #         businessItem = YellowpagesItem()
    #         businessItem['Name']   = hxs.xpath(businessXPath + suffixBusinessName).extract()
    #         businessItem['Street'] = hxs.xpath(businessXPath + suffixBusinessStreet).extract()
    #         businessItem['Postal'] = hxs.xpath(businessXPath + suffixBusinessPostal).extract()
    #         businessItem['Phone']  = hxs.xpath(businessXPath + suffixBusinessPhone).extract()

    #         businesses.append(businessItem)

    #     return businesses
        
    # def parse(self, response):
    #     yield Request(response.url, callback = self.parse_business_listings_page)

    # def parse_business_listings_page(self, response):
    #     print "Visiting %s" % response.url

    #     self.businesses.append(self.extract_businesses_from_response(response))
    #     hxs = Selector(response)
    #     li_tags = hxs.xpath('//*[@id="main-content"]/div[4]/div[5]/ul/li')
    #     next_exist = False
        
    #     # Check to see if there's a "Next". If there is, store the links.
    #     # If not, return. 
    #     # This requires a linear search through the list of li_tags. Is there a faster way?
    #     for li in li_tags:
    #         li_text = li.xpath('.//a/text()').extract()
    #         li_data_page = li.xpath('.//a/@data-page').extract()
    #         # Note: sometimes li_text is an empty list so check to see if it is nonempty first
    #         if (li_text and li_text[0] == 'Next'):
    #             next_exist = True
    #             next_page_num = li_data_page[0]

    #     if next_exist:
    #         for li in li_tags:
    #             li_text = li.xpath('.//a/text()').extract()
    #             li_href = li.xpath('.//a/@href').extract()
    #             li_data_page = li.xpath('.//a/@data-page').extract()
    #             if (li_data_page and li_data_page[0] == next_page_num and li_href):
    #                 url = self.base_url + li_href[0]
    #                 yield Request(url, callback=self.parse_business_listings_page)

