from scrapy.contrib.spiders import CrawlSpider, Rule
#from scrapy.contrib.exporter import JsonItemExporter
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy import Selector
from yellowPages.items import YellowpagesItem
from scrapy.http import Request

import json

class YellowPageSpider(CrawlSpider):
    name = "yellowpages_v2.com"
    allowed_domains = ["www.yellowpages.com"]
    businesses = []
    # start with one page
    start_urls = [
        "http://www.yellowpages.com/tucson-az/cupcakes?g=tucson%2C%20az&q=cupcakes",
        ]

# rules aren't needed....I wonder why
 #    rules = (
# #        Rule(LxmlLinkExtractor(allow=('//page=\d*',),
# #                               restrict_xpaths=('//*[@id="main-content"]/div[4]/div[5]/ul',)),
# #                               callback='parse_page', follow=True),
#         Rule(LxmlLinkExtractor(allow=('relevance&page=\d$',),
#                                restrict_xpaths=('//*[@id="main-content"]/div[4]/div[5]/ul/li[5]/a[@class="next ajax-page"]',)),
#                                callback='parse_page', follow=True),
#         )

    def extractBusinessesFromResponse(self,response):
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
        yield Request(response.url, callback = self.parse_page)

    def parse_page_get_next_page_link(self, li_tags, page_num):
        pageLinks = []
        for p in li_tags.xpath('.//li/a[contains(@href, "page")]'):
            link = p.xpath('@href').extract()[0]
            pageLinks.append(link)
            print type(link)

    def parse_page(self, response):
        print "Visiting %s" % response.url

        self.businesses.append(self.extractBusinessesFromResponse(response))
        hxs = Selector(response)
        li_tags = hxs.xpath('//*[@id="main-content"]/div[4]/div[5]/ul/li')
        
        # Check to see if there's a "Next". If there is, store the links.
        # If not, return.
        for li in li_tags:
            li_text = li.xpath('.//a/text()').extract()
            # Note: sometimes li_text is an empty list so check to see if it is nonempty first
            if (li_text and li_text[0] == 'Next'):
                next_num = li.xpath('.//a/@data-page').extract()[0]
                # Assumption: that the URL has this form
                url = 'http://www.yellowpages.com/tucson-az/cupcakes?g=tucson%2C%20az&q=cupcakes&s=relevance&page=' + next_num
                yield Request(url, callback=self.parse_page)

        # pageLinks = []
        # for p in li_tags.xpath('.//a[contains(@href, "page")]'):
        #     link = p.xpath('@href').extract()[0]
        #     pageLinks.append(link)

        # hxs = Selector(response)
        # something = hxs.xpath('//ul').extract()
        # print something
        # visitedLinks = set() # keep track of the URLs that we've already visited
        # print type(hxs)
        # businesses = self.extractBusinessesFromResponse(response)

        # return businesses
        # nextURL = hxs.xpath('//*[@id="main-content"]/div[4]/div[5]/ul/li[2]/a/@href').extract()[0]
        # yield Request(nextURL, callback=self.parse_page,)
