import scrapy


class GlassesSpider(scrapy.Spider):
  name = 'glasses'
  allowed_domains = ['www.glassesshop.com']
  start_urls = ['https://www.glassesshop.com/bestsellers']

  def parse(self, response):
    glasses = response.xpath("//div[contains(@class, 'product-list-item') and not(contains(@class, 'ad-banner'))]")
    for glass in glasses:
      yield {
          'product_url': glass.xpath(".//a[contains(@class, 'product-img')][1]/@href").get(),
          'product_image_link': glass.xpath(".//a[contains(@class, 'product-img')][1]/img[1]/@data-src").get(),
          'product_name': glass.xpath(".//a[contains(@class, 'product-title')][1]/@title").get(),
          'product_price': glass.xpath(".//div[contains(@class, 'p-price')]/div[1]/span/text()").get()
      }

    next_page = response.xpath("//a[@rel='next']/@href").get()
    if next_page:
      yield scrapy.Request(url=next_page, callback=self.parse)
