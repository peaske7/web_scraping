import time
from collections import Counter
from urllib import robotparser

import requests
from bs4 import BeautifulSoup
from tld import get_fld
from tld import get_tld


def get_rb_object(url):
    robot_url = get_robot_url(url)
    rp = robotparser.RobotFileParser()
    rp.set_url(robot_url)
    rp.read()
    return rp


def parse_robot(url, rb_object):
    flag = rb_object.can_fetch("*", url)
    try:
        crawl_d = rb_object.crawl_delay("*")
    except Exception as E:
        crawl_d = None
    return flag, crawl_d


def get_robot_url(url):
    res = get_tld(url, as_object=True)
    final_url = res.parsed_url.scheme + '://' + res.parsed_url.netloc + '/robots.txt'
    return final_url


def get_normalized_url(url):
    res = get_tld(url, as_object=True)
    path_list = [char for char in res.parsed_url.path]
    if len(path_list) == 0:
        final_url = res.parsed_url.scheme + '://' + res.parsed_url.netloc
    elif path_list[-1] == '/':
        final_string = ''.join(path_list[-1])
        final_url = res.parsed_url.scheme + '://' + res.parsed_url.netloc + final_string
    else:
        final_url = url
    return final_url


def advanced_link_crawler(seed_url, max_n=5000):
    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36' +
                      ' (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    }
    initial_url_set = set()
    initial_url_list = []
    seen_url_set = set()
    base_url = 'http://www.' + get_fld(seed_url)

    res = get_tld(seed_url, as_object=True)
    domain_name = res.fld

    initial_url_set.add(seed_url)
    initial_url_list.append(seed_url)

    robot_object = get_rb_object(seed_url)
    flag, delay_time = parse_robot(seed_url, robot_object)

    if delay_time is None:
        delay_time = 0.1

    if flag is False:
        print('crawling not permitted')
        return initial_url_set, seen_url_set

    while len(initial_url_set) != 0 and len(seen_url_set) < max_n:
        temp_url = initial_url_set.pop()
        if temp_url in seen_url_set:
            continue
        else:
            seen_url_set.add(temp_url)
            time.sleep(delay_time)
            r = requests.get(url=temp_url, headers=my_headers)
            st_code = r.status_code
            if st_code != 200:
                time.sleep(delay_time)
                r = requests.get(url=temp_url, headers=my_headers)
                if r.status_code != 200:
                    continue
            print(st_code)
            html_response = r.text
            soup = BeautifulSoup(html_response)
            links = soup.find_all('a', href=True)
            for link in links:
                print(link['href'])
                if 'http' in link['href']:
                    if domain_name in link['href']:
                        final_url = link['href']
                    else:
                        continue
                elif [char for char in link['href']][0] == '/':
                    final_url = base_url + link['href']
                    # insert url normalization
                    final_url = get_normalized_url(final_url)
                    flag, delay = parse_robot(seed_url, robot_object)
                    # insert robot file checking
                    if flag is True:
                        initial_url_set.add(final_url.strip())
                        initial_url_list.append(final_url.strip())

    counted_dict = Counter(initial_url_list)
    return initial_url_set, counted_dict


seed_url = 'http://www.jaympatel.com'
advanced_link_crawler(seed_url)
