import json
import os.path
import random
from time import sleep

import requests

fname = "./the.all_endpoints.txt"


def read(fname):
    f = open(fname, "r")
    endpoints = f.readlines()
    return endpoints


def call_endpoints(endpoints_list):
    length = len(endpoints_list)
    i = 0
    headers = {
        "Cookie": "geoCountry=JP; siteCountry=GB",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
        "referer": "https://www.timeshighereducation.com/world-university-rankings/2021/world-ranking",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Connection": "keep-alive",
    }
    payload = {}

    error_endpoints = []

    while i < length:
        url = endpoints_list[i].strip()
        split_url = url.replace("the_data_rankings/", "_0__").split("_0__")
        group_and_year_string = split_url[1].split("_")
        ranking_group = "_".join(group_and_year_string[:-1])
        year = group_and_year_string[-1]
        new_fname = f"./layer_1/{ranking_group}.{year}.json"

        # if file does not exist, fetch and create new file
        if not os.path.isfile(new_fname):
            sleep(random.randrange(2,5))
            response = requests.request(
                "GET",
                url=url,
                headers=headers,
                data=payload,
            )
            if response.text == '404: Not Found.':
                print(f"404 response for {new_fname}")
                error_endpoints.append(new_fname)
            else:
                with open(new_fname, "w+") as outfile:
                    outfile.write(response.text.encode().decode("unicode-escape"))
                print(f"{new_fname} successfully created!")
                if new_fname in error_endpoints:
                    error_endpoints.remove(new_fname)
        else:
            print(f"file {new_fname} already exists")
        i += 1

    errors_fname = 'layer_1_error_endpoints.json'
    with open(errors_fname, 'w+') as errorfile:
        errorfile.write(json.dumps(error_endpoints))

    # call again ?


def main():
    call_endpoints(read(fname))


main()
