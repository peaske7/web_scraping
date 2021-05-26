import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'

    def start_requests(self):
      yield scrapy.Request(url="https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc", headers={
        'User-Agent': self.user_agent
      })

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3[@class="lister-item-header"]/a'), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths='(//a[@class="lister-page-next next-page"])[2]'), process_request='set_user_agent')
    )

    def set_user_agent(self, request, spider):
      request.headers['User-Agent'] = self.user_agent
      return request

    def parse_item(self, response):
        yield {
          'title': response.xpath("//div[@class='title_wrapper']/h1/text()").get(),
          'durationg': response.xpath("normalize-space((//time)[1]/text())").get(),
          'movie_url': response.url
        }
