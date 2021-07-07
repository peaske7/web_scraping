import scrapy
from scrapy_splash import SplashRequest

class SchoolRankingSpider(scrapy.Spider):
    name = 'school_ranking'
    allowed_domains = ['roundranking.com']

    script = '''
      function main(splash, args)
        splash.private_mode_enabled=false
        
        url = args.url
        assert(splash:go(url))
        assert(splash:wait(2))
        
        return splash:html()
      end
    '''

    def start_requests(self):
      yield SplashRequest(url='https://roundranking.com/ranking/world-university-rankings.html#world-2010', callback=self.parse, endpoint='execute',args={
        'lua_source': self.script
      })

    def parse(self, response):
      current_year = int(response.xpath("//a[@class='point active']/span[2]/text()").get())
      for school in response.xpath("//tbody/tr"):
        yield {
          'year': current_year,
          'name': school.xpath(".//td[2]/a/text()").get(),
          'ranking': school.xpath(".//td[1]/text()").get(),
          'score': school.xpath(".//td[3]/text()").get(),
        }

      if (current_year < 2021):
        yield SplashRequest(url=f"https://roundranking.com/ranking/world-university-rankings.html#world-{current_year+1}", callback=self.parse, endpoint='execute', args={
          'lua_source': self.script
        })
