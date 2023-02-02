import scrapy

class SampleItem(scrapy.Item):
    title = scrapy.Field()
    text = scrapy.Field()
    url_id=scrapy.Field()