import scrapy


class MySpiderSpider(scrapy.Spider):
    name = "my_spider"
    allowed_domains = ["google.com"]
    start_urls = ["http://google.com/"]

    def parse(self, response):
        pass
