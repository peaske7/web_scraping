import scrapy


class CollegeRankingsSpider(scrapy.Spider):
    name = "college_rankings"
    allowed_domains = ["cwur.org"]
    url = "https://cwur.org/2021-22/country/usa.php"

    # randomly cycle through different variables in the header
    # ====== PHP pages are not scrapable with python dugh ======

    my_headers = {
        ":authority": "cwur.org",
        ":method": "GET",
        ":path": "/2021-22/country/usa.php",
        ":scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
    }

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse, headers=self.my_headers)

    def parse(self, response):
        title = response.xpath("//div[@class='page-header']/h4/text()").get()
        yield {"title": title}
