from scrapy import Item, Field
__author__ = 'tao'

class PadItem(Item):
    sno = Field()
    price = Field()

class ReviewItem(Item):
    user = Field()
    item = Field()
    rate = Field()
    text = Field()
    time = Field()
