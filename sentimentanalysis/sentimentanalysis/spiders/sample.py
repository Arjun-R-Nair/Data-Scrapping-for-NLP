import scrapy
import os
import csv
from items import SampleItem

class SampleSpider(scrapy.Spider):
    name = 'sample'
    allowed_domains = ['insights.blackcoffer.com']
    def start_requests(self):
        with open("Input.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                url_id = row[0]
                url = row[1]
                yield scrapy.Request(url, self.parse, meta={'url_id': url_id})

    def parse(self, response):
        url_id = response.meta['url_id']
        item = SampleItem()
        item['title'] = response.css('h1::text').get()
        item['text'] = response.css('p::text').extract()
        item['url_id']=url_id
        yield item
        directory = "data"
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = os.path.join(directory, f"{url_id}.txt")
        with open(os.path.join(directory,f"{item['url_id']}.txt"), "w") as f:
            content = f"TITLE: {item['title']}\nTEXT: {item['text']}\n"
            f.write(content)