from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from yellowPages.items import YellowpagesItem
from scrapy.http import Request

class YellowPageSpider(CrawlSpider):
    name = "yellowpages_v2.com"
    allowed_domains = ["yellowpages.com"]
    # start with one page
    start_urls = [
        "http://www.yellowpages.com/tucson-az/cupcakes?g=tucson%2C%20az&q=cupcakes"
        ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('//ul/li[\d]/a',),
                               restrict_xpaths=('//*[@id="main-content"]/div[4]/div[5]/',)),
                               callback='parse_page', follow=True),
        )
    def parse(self, response):
        self.parse_page(response)
        businesses = []

        hxs = HtmlXPathSelector(response)
        businessIDs = hxs.select('//*[@id="main-content"]/div[4]/div[3]/div/@id').extract()

        for business in businessIDs:
            businessXPath = '//*[@id="'+business+'"]/div/div[2]/div[2]'
            suffixBusinessName    = '/h3/a[1]/span/text()'
            suffixBusinessStreet  = '/div/div[1]/p/span[1]/text()'
            suffixBusinessPostal  = '/div/div[1]/p/span[4]/text()'
            suffixBusinessPhone   = '/div/div[1]/ul/li/text()'

            businessItem = YellowpagesItem()
            businessItem['businessName']   = hxs.select(businessXPath + suffixBusinessName).extract()
            businessItem['businessStreet'] = hxs.select(businessXPath + suffixBusinessStreet).extract()
            businessItem['businessPostal'] = hxs.select(businessXPath + suffixBusinessPostal).extract()
            businessItem['businessPhone']  = hxs.select(businessXPath + suffixBusinessPhone).extract()

            businesses.append(businessItem)

        # liTags = hxs.select('//*[@id="main-content"]/div[4]/div[5]/ul').extract()
        
        # for li in liTags:
        #     print type(li)
        #     print li.select('./a/@href').extract()

        nextURL = hxs.select('//*[@id="main-content"]/div[4]/div[5]/ul/li[2]/a/@href').extract()[0]
        print "next page is %s " % nextURL
        nextURL = "www.yellowpages.com"+nextURL
        print "next page is %s " % nextURL
        if nextURL:
            request = Request(url=nextURL, callback=self.parse_page,)
        return businesses

    def parse_page(self, response):
        print "Visited 2nd page!"

        businesses = []

        hxs = HtmlXPathSelector(response)
        businessIDs = hxs.select('//*[@id="main-content"]/div[4]/div[3]/div/@id').extract()

        for business in businessIDs:
            businessXPath = '//*[@id="'+business+'"]/div/div[2]/div[2]'
            suffixBusinessName    = '/h3/a[1]/span/text()'
            suffixBusinessStreet  = '/div/div[1]/p/span[1]/text()'
            suffixBusinessPostal  = '/div/div[1]/p/span[4]/text()'
            suffixBusinessPhone   = '/div/div[1]/ul/li/text()'

            businessItem = YellowpagesItem()
            businessItem['businessName']   = hxs.select(businessXPath + suffixBusinessName).extract()
            businessItem['businessStreet'] = hxs.select(businessXPath + suffixBusinessStreet).extract()
            businessItem['businessPostal'] = hxs.select(businessXPath + suffixBusinessPostal).extract()
            businessItem['businessPhone']  = hxs.select(businessXPath + suffixBusinessPhone).extract()

            businesses.append(businessItem)

        nextURL = hxs.select('//*[@id="main-content"]/div[4]/div[5]/ul/li[2]/a/@href').extract()[0]
        yield Request(nextURL, callback=self.parse_page,)
