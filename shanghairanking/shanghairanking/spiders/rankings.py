import scrapy


class RankingsSpider(scrapy.Spider):
    name = 'rankings'
    allowed_domains = ['shanghairanking.com']
    start_urls = ['http://shanghairanking.com/']

    def start_requests(self):
			pass
