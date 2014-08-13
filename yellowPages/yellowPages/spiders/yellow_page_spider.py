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
        for business in businessIDs:
            businessXPath = '//*[@id="'+business+'"]/div/div[2]/div[2]'
            suffixBusinessName    = '/h3/a[1]/span/text()'
            suffixBusinessStreet  = '/div/div[1]/p/span[1]/text()'
            suffixBusinessPostal  = '/div/div[1]/p/span[4]/text()'
            suffixBusinessPhone   = '/div/div[1]/ul/li/text()'

            item = YellowpagesItem()
            item['businessName']   = hxs.select(businessXPath + suffixBusinessName).extract()
            item['businessStreet'] = hxs.select(businessXPath + suffixBusinessStreet).extract()
            item['businessPostal'] = hxs.select(businessXPath + suffixBusinessPostal).extract()
            item['businessPhone']  = hxs.select(businessXPath + suffixBusinessPhone).extract()
            print item['businessName']
            print item['businessStreet']
            print item['businessPostal']
            print item['businessPhone']
        # sites = hxs.select('//*[@id="main-content"]/div[4]/div[3]/div/@id').extract()
        # for site in sites:
        #     print site.select('./@id').extract()
            # item = YellowpagesItem()
            # item['title'] = site.select('text()').extract()
            # print item['title']
        # filename = "cupcakes"
        # open(filename, 'wb').write(response.body)
