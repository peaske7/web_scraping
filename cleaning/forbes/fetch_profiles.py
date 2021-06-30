import os.path
import random
import requests
import json
from lxml import html
from time import sleep

json_fname = "./forbes_university_ranking.2019.json"


def read(fname):
    f = open(fname, "r")
    data = json.load(f)
    schools = data["organizationList"]["organizationsLists"]
    return schools


def fetch_profiles(schools):
    # hard coded stuff needed for requests
    payload = {}
    headers = {
        "Cookie": "geoCountry=JP; siteCountry=GB; has_js=1; cookie-agreed-version=1.0.0; studentWallNag=true; __tesu=60c1d079-28b2-4eb7-81de-affc2dd22ddb; _ga=GA1.2.1870236577.1622007534; __Host-next-auth.csrf-token=6f6bbb3d80398220391a5b1ec1b97bdcefa294f36ed8633c07125f4d4e4d3014%7Ceade51387a8aead3bfced8ca3cdefdff5110d2db1a73bffc0c738487ef15dc0a; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.timeshighereducation.com%2Fstudent; _hjTLDTest=1; _hjid=89a57070-e572-444c-b32c-a6603b3acc83; _gid=GA1.2.227047130.1624159077; __tesv=1918d4df-b86f-40bf-9422-c5bd237d8e4a; cookie-agreed=2; SSESS411abc56fecd6d2addc06cd71ed283ee=osalLHQuK_sjtg-eAK6zLKJQfCVwWup4vFpI5igJHxM; Drupal.visitor.login_history=447b9d57937fdd8e4d1e888aef3cc132877ad1c574a341c2788697114d730a53-7b6ca9b1d047cae334cce5ced5e1db2f41f3a61eceb76607d86bdefe675a858b-3048500; Drupal.visitor.path=%2F; Drupal.visitor.the_user=%7B%22show_menu%22%3A0%2C%22user_closed%22%3A1%7D; __tess=rankings_table%7C%7C16",
        "Referer": "https://google.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
    }

    # params for while loop
    i = 0
    while i < len(schools):
        school_uri = schools[i]["uri"]
        full_uri = f"https://www.forbes.com/colleges/{school_uri}"
        new_fname = f"./layer_1/{school_uri.replace('-','_')}.2019.json"

        # make file, if file doesn't exists. If not, skip. Sleep here.
        if not os.path.isfile(new_fname):
            sleep(random.uniform(2.0, 7.0))
            response = requests.request(
                "GET",
                url=full_uri,
                headers=headers,
                data=payload,
            )

            rankings = {
                "school_name": f"{school_uri.replace('-', ' ')}",
                "school_forbes_uri": school_uri,
                "school_forbes_abs_uri": full_uri,
                "rankings": [],
            }

            # scraping
            scrape_forbes_profile(response.text, rankings)
            with open(new_fname, "w+") as outfile:
                outfile.write(json.dumps(rankings))
            print(f"#{i}/{len(schools)}|| success! file {new_fname} created")

        else:
            print(f"#{i}/{len(schools)}|| file {new_fname} already exists")
        i += 1


def scrape_forbes_profile(response_text, rankings):
    tree = html.fromstring(response_text)
    rankings_list = tree.xpath("//div[@class='profile-list__item']")
    for ranking in rankings_list:
        ranking_value = ranking.xpath(".//div[@class='profile-list__rank']/text()")
        ranking_name = ranking.xpath(
            ".//*[not(contains(@class,'profile-list__rank'))]/text()"
        )
        # if both values exist (none are empty strings)
        if len(ranking_value) and len(ranking_name):
            rankings["rankings"].append(
                {
                    "category_name": ranking_name[0],
                    "category_ranking": ranking_value[0].replace("#", ""),
                }
            )
        else:
            print("skipped because one or both values contain empty string")


def main():
    # read(json_fname)
    fetch_profiles(read(json_fname))


main()
