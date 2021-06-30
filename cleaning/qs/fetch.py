import requests
from time import sleep
import random
import json
import os.path
import re

fname = "./qs.all_endpoints.txt"
layer_1_dirname = "./layer_1"
layer_2_dirname = "./layer_2"


def read(fname: str) -> str:
    # open and read file
    f = open(fname, "r")
    endpoints = f.readlines()

    # setting variables
    groups = []
    year_holder = ""
    index = -1

    # traverse file
    for string in endpoints:
        tabs_contained = string.split("\t")
        if len(tabs_contained) == 1:
            index += 1  # increment index for each full pass of ranking category
            category_name = (string.replace("&", "and").strip().replace(" ", "_"),)
            group = {
                "rankings_category": category_name[0],
                "rankings_by_year": [],
            }
            groups.append(group)

        elif len(tabs_contained) == 2:
            year_holder = tabs_contained[1].strip()

        elif len(tabs_contained) == 3:
            yearly_ranking = {
                "year": year_holder,
                "endpoint": tabs_contained[2].strip(),
            }
            groups[index]["rankings_by_year"].append(yearly_ranking)

    data = json.dumps(groups)
    return data


def call_endpoints(data: str) -> None:
    loaded_data = json.loads(data)

    # info for get request to endpoint
    headers = {
        "Cookie": "geoCountry=JP; siteCountry=GB",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
        "Accept": "*/*",
        "Connection": "keep-alive",
    }
    payload = {}

    for group in loaded_data:
        category_name = group["rankings_category"]

        for ranking in group["rankings_by_year"]:
            ranking_year = ranking["year"]
            ranking_url = ranking["endpoint"]
            new_fname = f"./layer_1/{category_name}.{ranking_year}.txt"

            if not os.path.isfile(new_fname):
                sleep(random.random() * 4)
                response = requests.request(
                    "GET",
                    url=ranking_url,
                    headers=headers,
                    data=payload,
                )
                with open(new_fname, "w+") as outfile:
                    outfile.write(response.text.encode().decode("unicode-escape"))
                print(f"success! file {new_fname} created!")
            else:
                print(f"file {new_fname} already exists")


def clean_layer_1(dirname) -> None:
    for subdir, dirs, files in os.walk(dirname):
        for file in files:
            fname = f"{subdir}/{file}"
            f = open(fname, "r")
            fcontent = f.read()
            json_file = re.split(".txt", file)[0]
            new_fname = f"./layer_2/{json_file}.json"
            title_regex = '<div class="td-wrap"><a href="[^"]{1,}" class="uni-link">[^<]{1,}<\\\/a><\\\/div>'
            results = re.findall(title_regex, fcontent)
            for result in results:
                school_name = re.split('<\\\\/a|class="uni-link">', result)[1]
                school_name = school_name.replace('"', "")
                fcontent = fcontent.replace(result, school_name)

            if not os.path.isfile(new_fname):
                with open(new_fname, "w+") as outfile:
                    outfile.write(fcontent)
                print(f"success! file {new_fname} created!")
            else:
                print(f"file {new_fname} already exists")


def clean_layer_2(dirname: str) -> None:
    for subdir, dirs, files in os.walk(dirname):
        for file in files:
            # load data from file
            fname = f"{subdir}/{file}"
            f = open(fname, "r")
            fcontent = f.read()
            loaded_data = json.loads(fcontent)
            schools = loaded_data["data"]

            # create a new python object and create new json file from that object
            cleaned_data = []
            new_fname = f"./layer_3/{file}"

            # get year and ranking category
            year_and_category = re.split("\.", file)
            year = year_and_category[1]
            category = year_and_category[0]

            for school in schools:
                school_obj = {
                    "year": year,
                    "category": category,
                    "rank": school["rank_display"],
                    "name": school["title"],
                    "country": school["country"],
                    "score": school["score"],
                }
                cleaned_data.append(school_obj)

            # create new file for cleaned_data, if not yet created
            if not os.path.isfile(new_fname):
                with open(new_fname, "w+") as outfile:
                    outfile.write(json.dumps(cleaned_data))
                print(f"success! file {new_fname} created!")
            else:
                print(f"file {new_fname} already exists")


def main():
    # call_endpoints(read(fname))
    # clean_layer_1(layer_1_dirname)
    clean_layer_2(layer_2_dirname)


main()
