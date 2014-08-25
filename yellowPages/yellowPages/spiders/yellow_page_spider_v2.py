"""
This module extends CrawlSpider and crawls through a Yellow Page set of results
based on a category and (city, state) query. 

For every page of results, the YellowPageSpider crawls and scrapes specific
business listings and returns the resulting item.
"""

from scrapy.contrib.spiders import CrawlSpider, Rule
#from scrapy.contrib.exporter import JsonItemExporter
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import Selector
from yellowPages.items import YellowpagesItem
from scrapy.http import Request, FormRequest

class YellowPageSpider(CrawlSpider):
    name = "yellowpages"
    allowed_domains = ['www.yellowpages.com']
    base_url = 'http://www.yellowpages.com'

    #
    # Customizable parameters for the query
    #
    category = 'cupcakes'
    location = 'tucson, az'

    #
    # Form initial query
    #
    # url = base_url+'/'+city+'-'+state+'/'+category
    # start_urls = [url]

    #
    # Create rules for the spider:
    # 1st Rule: to crawl through different page results of listings that match
    #           the query
    # 2nd Rule: to crawl through the business-specific listing link
    #
    rules = (
             Rule(SgmlLinkExtractor(allow=('page=\d$',),),
                  follow=True),
             Rule(SgmlLinkExtractor(allow=('\d+\?lid=\d+$',),),
                  callback='parse_business_page', follow=True),
    )

    def start_requests(self):
        yield FormRequest("http://www.yellowpages.com/search/", method='GET',
                          formdata={'search_terms':self.category, 'geo_location_terms':self.location},
                          callback=self.parse)

    # 
    # Function: parse_business_page - Callback to scrape information specific to
    #           business listing
    # 
    # parameters: 
    #  - self - reference to object
    #  - response - HTTP response
    #
    def parse_business_page(self, response):
        #
        # Set up xpaths for populating item entries
        #
        hxs               = Selector(response)
        contact           = hxs.xpath('//*[@id="main-content"]/div[1]/div[1]/div/section[2]/div[1]')
        bNameXPath_list   = hxs.xpath('//*[@id="main-content"]/div[1]/div[1]/h1/text()').extract()        
        bStreetXPath_list = contact.xpath('./p[@class="street-address"]/text()').extract()
        bCityState_list   = contact.xpath('./p[@class="city-state"]/text()').extract()
        bPhone_list       = contact.xpath('./p[@class="phone"]/text()').extract()

        #
        # Grab specific business fields
        #
        businessItem           = YellowpagesItem()
        businessItem['Name']   = bNameXPath_list[0] if bNameXPath_list else ''
        businessItem['Street'] = bStreetXPath_list[0] if bStreetXPath_list else ''
        businessItem['Phone']  = bPhone_list[0] if bPhone_list else ''
        if bCityState_list:
            city_state_string      = bCityState_list[0]
            businessItem['City'], businessItem['State'], businessItem['Postal'] = city_state_string.split()
            businessItem['City'] = businessItem['City'].strip(',')
            businessItem['Postal'] = int(businessItem['Postal'])
            businessItem['Street'] = businessItem['Street'].strip(',')
        else:
            city_state_string = ''

        return businessItem

