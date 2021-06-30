import scrapy
from urllib.parse import urlencode
from scrapy_splash import SplashRequest

API_KEY = "cb5d118e3a19ec7957426724bd3e540b"


def get_scraperapi_url(url):
    payload = {"api_key": API_KEY, "url": url}
    proxy_url = "http://api.scraperapi.com/?" + urlencode(payload)
    return proxy_url


class RankingsSpider(scrapy.Spider):
    name = "rankings"
    allowed_domains = ["www.shanghairanking.com"]

    http_user = "user"
    http_pass = "userpass"

    current_page = 1
    max_pages = 4

    current_year = 2020
    starting_year = 2003

    schools_list = []

    _initial_script = """
        function main(splash, args)
            splash:on_request(function(request)
                if request.url:find('css') then
                    request.abort()
                end
            end)
            splash.images_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(0.2))
            splash:set_viewport_full()
            return splash:html()
        end
    """

    my_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "*",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "www.shanghairanking.com",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0",
        "Referer": "http://www.shanghairanking.com/",
    }

    def start_requests(self):
        yield SplashRequest(
            url=get_scraperapi_url("http://www.shanghairanking.com/rankings/arwu/2020"),
            endpoint="execute",
            callback=self.parse_page,
            args={"lua_source": self._initial_script},
            headers=self.my_headers,
        )

    def parse_page(self, response):
        schools = response.xpath("//tbody/tr")
        for school in schools:
            country_img_element = school.xpath(
                "normalize-space(.//div[@class='region-img']/@style)"
            ).get()
            country = country_img_element.split("/")[-1].split(".")[0]
            if country == "us":
                world_ranking = school.xpath(
                    "normalize-space(.//div[contains(@class, 'ranking')]/text())"
                ).get()
                name = school.xpath(
                    "normalize-space(.//span[@class='univ-name']/text())"
                ).get()
                national_ranking = school.xpath(
                    "normalize-space(.//td[4]/text())"
                ).get()
                print(name)
                yield {
                    "year": self.current_year,
                    "world_ranking": world_ranking,
                    "name": name,
                    "national_ranking": national_ranking,
                }
        self.current_page += 1
        if self.current_page <= self.max_pages:
            print(self.current_page)
            _script_head = """
                function main(splash, args)
                    splash:on_request(function(request)
                        if request.url:find('css') then
                            request.abort()
                        end
                    end)
                    splash.images_enabled = false
                    assert(splash:go(args.url))
                    assert(splash:wait(0.2))
                    splash:set_viewport_full()
                    local get_dims = splash:jsfunc([[
                        function() {
                            var rect = document.getElementsByClassName('ant-pagination-next')[0].getClientRects()[0]
                            return {"x": rect.left, "y": rect.top}
                        }
                    ]])
                    local dims = get_dims()\n
                """
            _script_body = """splash:mouse_click(dims.x, dims.y)
                    assert(splash:wait(0.2))\n"""
            _script_tail = """
                    return splash:html()
                end 
            """
            _script = _script_head
            for i in range(1, self.current_page):
                _script += _script_body
            _script += _script_tail
            print(_script)

            yield SplashRequest(
                url=get_scraperapi_url(
                    "http://www.shanghairanking.com/rankings/arwu/2020"
                ),
                endpoint="execute",
                callback=self.parse_page,
                args={"lua_source": _script},
                headers=self.my_headers,
            )
