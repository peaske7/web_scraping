import scrapy


class GdpDebtSpider(scrapy.Spider):
    name = 'gdp_debt'
    allowed_domains = ['worldpopulationreview.com/countries/countries-by-national-debt']
    start_urls = ['http://worldpopulationreview.com/countries/countries-by-national-debt/']

    # yield country_name and gdp_debt

    def parse(self, response):
      countries = response.xpath("//tbody/tr")
      for country in countries:
        name = country.xpath(".//td/a/text()").get()
        gdp_debt = country.xpath(".//td[3]/text()").get()

        yield {
          'country_name': name,
          'gdp_debt': gdp_debt
        }
