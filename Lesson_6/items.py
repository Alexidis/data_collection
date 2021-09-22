import scrapy


class LeruaItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    photos = scrapy.Field()
    characteristics = scrapy.Field()
    pass
