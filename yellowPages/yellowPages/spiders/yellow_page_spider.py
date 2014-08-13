from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from yellowPages.items import YellowpagesItem

class YellowPageSpider(BaseSpider):
    name = "yellowpages.com"
    allowed_domains = ["yellowpages.com"]
    start_urls = [
        "http://www.yellowpages.com/tucson-az/cupcakes?g=tucson%2C%20az&q=cupcakes"
        ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('///div')
        for site in sites:
            item = YellowpagesItem()
            item['title'] = site.select('text()').extract()
            print item['title']
        # filename = "cupcakes"
        # open(filename, 'wb').write(response.body)
