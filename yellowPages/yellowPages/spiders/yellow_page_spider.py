from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

class YellowPageSpider(BaseSpider):
    name = "yellowpages.com"
    allowed_domains = [
        "http://www.yellowpages.com/tucson-az/cupcakes?g=tucson%2C%20az&q=cupcakes"
        ]

    def parse(self, response):
        filename = "cupcakes"
        open(filename, 'wb').write(response.body)
