from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from yellowPages.items import YellowpagesItem

class YellowPageSpider(BaseSpider):
    name = "yellowpages.com"
    allowed_domains = ["yellowpages.com"]
    # start with one page
    start_urls = [
        "http://www.yellowpages.com/tucson-az/cupcakes?g=tucson%2C%20az&q=cupcakes"
        ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        businessIDs = hxs.select('//*[@id="main-content"]/div[4]/div[3]/div/@id').extract()

        businesses = []
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
            # print businessItem['businessName']
            # print businessItem['businessStreet']
            # print businessItem['businessPostal']
            # print businessItem['businessPhone']

            businesses.append(businessItem)

        return businesses
