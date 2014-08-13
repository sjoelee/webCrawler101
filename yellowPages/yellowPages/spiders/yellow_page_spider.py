from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

class YellowPageSpider(BaseSpider):
    name = "yellowpages.com"
    allowed_domains = ["yellowpages.com"]
    start_urls = [
        "http://www.yellowpages.com/tucson-az/cupcakes?g=tucson%2C%20az&q=cupcakes",
#        "http://www.yellowpages.com/tucson-az/mip/cupcakes-456735205?lid=456735205"
        ]

    def parse(self, response):
#        filename = response.url.split("/")[-2]#"cupcakes"
        filename = "cupcakes"
        open(filename, 'wb').write(response.body)
