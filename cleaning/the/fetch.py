import requests
from time import sleep
import random
import os.path

fname = "./the.all_endpoints.txt"


def read(fname):
    f = open(fname, "r")
    endpoints = f.readlines()
    print(len(endpoints))
    return endpoints


def call_endpoints(endpoints_list):
    length = len(endpoints_list)
    i = 0
    headers = {
        "Cookie": "geoCountry=JP; siteCountry=GB",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
        "referer": "https://www.timeshighereducation.com/world-university-rankings/2021/world-ranking",
        "Accept": "*/*",
        "Connection": "keep-alive",
    }
    payload = {}

    while i < length:
        url = endpoints_list[i].strip()
        split_url = url.replace("the_data_rankings/", "_0__").split("_0__")
        group_and_year_string = split_url[1].split("_")
        ranking_group = "_".join(group_and_year_string[:-1])
        year = group_and_year_string[-1]
        new_fname = f"./layer_1/{ranking_group}.{year}.json"

        # if file does not exist, fetch and create new file
        if not os.path.isfile(new_fname):
            sleep(random.random() * 4)
            response = requests.request(
                "GET",
                url=url,
                headers=headers,
                data=payload,
            )
            with open(new_fname, "w+") as outfile:
                outfile.write(response.text.encode().decode("unicode-escape"))
        # if file exists, skip
        else:
            print(f"file {new_fname} already exists")

        i += 1


def main():
    call_endpoints(read(fname))


main()
