# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
from scrapy.item import Item, Field

class YellowpagesItem(Item):
    # define the fields for your item here like:
    # name = Field()
    Name = Field()
    Street = Field()
    Postal = Field()
    City = Field()
    State = Field()
    Phone = Field()
    Cat = Field()
    Hours = Field()
