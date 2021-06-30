import scrapy
import random
import json
from time import sleep


class AllCollegeLinksSpider(scrapy.Spider):
    name = "all_college_links"

    url = "https://www.niche.com/colleges/search/all-colleges"
    headers = {}

    def start_requests(self):
        pass

    def parse(self, response):
        pass
