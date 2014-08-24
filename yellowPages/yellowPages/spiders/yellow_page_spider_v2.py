from scrapy.contrib.spiders import CrawlSpider, Rule
#from scrapy.contrib.exporter import JsonItemExporter
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import Selector
from yellowPages.items import YellowpagesItem
from scrapy.http import Request, FormRequest

import json

class YellowPageSpider(CrawlSpider):
    name = "yellowpages"
    allowed_domains = ['www.yellowpages.com']
    businesses = []
    count = 0
    num_request = 0

    start_urls = ['http://www.yellowpages.com/tucson-az/cupcakes?g=tucson%2C%20az&q=cupcakes',
    ]

    rules = (
             Rule(SgmlLinkExtractor(allow=('&page=\d$',),),
                  follow=True),
             Rule(SgmlLinkExtractor(allow=('\d+\?lid=\d+$',),),
                  callback='parse_business_page', follow=True),
    )

    base_url = 'http://www.yellowpages.com'

    def parse_business_page(self, response):
        hxs               = Selector(response)
        categories        = hxs.xpath('//*[@id="business-details"]/dl/dd[4]')
        contact           = hxs.xpath('//*[@id="main-content"]/div[1]/div[1]/div/section[2]/div[1]')
        bNameXPath_list   = hxs.xpath('//*[@id="main-content"]/div[1]/div[1]/h1/text()').extract()        
        bStreetXPath_list = contact.xpath('./p[@class="street-address"]/text()').extract()
        bCityState_list   = contact.xpath('./p[@class="city-state"]/text()').extract()
        bPhone_list       = contact.xpath('./p[@class="phone"]/text()').extract()

        businessItem               = YellowpagesItem()
        businessItem['Name']       = bNameXPath_list[0] if bNameXPath_list else ''
        businessItem['Street']     = bStreetXPath_list[0] if bStreetXPath_list else ''
        businessItem['City_State'] = bCityState_list[0] if bCityState_list else ''
        businessItem['Phone']      = bPhone_list[0] if bPhone_list else ''

        self.count = self.count + 1
        print self.count

        return businessItem

