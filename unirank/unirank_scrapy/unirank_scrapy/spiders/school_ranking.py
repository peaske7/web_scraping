import scrapy

class SchoolRankingSpider(scrapy.Spider):
    name = 'school_ranking'
    allowed_domains = ['www.4icu.org/']
    start_urls = ['http://www.4icu.org/us']

    def parse(self, response):
      schools = response.xpath('//table/tbody/tr')
      for school in schools:
        yield {
          'year': 2021,
          'name': school.xpath(".//td/a/text()").get(),
          'ranking': school.xpath(".//td/b/text()").get(),
        }
