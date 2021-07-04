import json
from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs, urlencode

URL = "https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A2%7D%2C%22usersSearchTerm%22%3A%22Miami%20Beach%2C%20FL%22%2C%22mapBounds%22%3A%7B%22west%22%3A-80.17009%2C%22east%22%3A-80.110191%2C%22south%22%3A25.747677%2C%22north%22%3A25.872806%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A5924%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D&wants={%22cat1%22:[%22listResults%22],%22cat2%22:[%22total%22]}&requestId=2"


def cookie_parser():
    cookie_string = 'zguid=23|%24036ecefd-3074-4f85-8c5f-d3ef5e148f06; zgsession=1|1d5ec0ef-485e-4213-a530-fa5a65ad5d02; _ga=GA1.2.44688170.1625361381; _gid=GA1.2.1406842477.1625361381; zjs_user_id=null; zjs_anonymous_id=%22036ecefd-3074-4f85-8c5f-d3ef5e148f06%22; _pxvid=716fad80-dc65-11eb-8828-0242ac12001a; _gcl_au=1.1.792230508.1625361383; KruxPixel=true; DoubleClickSession=true; __pdst=f88193bfd88b4ce69942f1c34d68cb83; KruxAddition=true; utag_main=v_id:017a6f1689950022608fca8e618203079001707100942$_sn:1$_se:1$_ss:1$_st:1625363185881$ses_id:1625361385881%3Bexp-session$_pn:1%3Bexp-session$dcsyncran:1%3Bexp-session$tdsyncran:1%3Bexp-session$dc_visit:1$dc_event:1%3Bexp-session$dc_region:ap-northeast-1%3Bexp-session$ttd_uuid:bef62f10-6d29-4291-898b-a8869ce12434%3Bexp-session; JSESSIONID=9BEC83B9F89DD9AB3B7BD255989BFB5A; g_state={"i_p":1625368729446,"i_l":1}; FSsampler=1010133865; _gat=1; _pxff_bsco=1; _uetsid=73bb9370dc6511ebb00215007147f5e6; _uetvid=73bfa970dc6511eb9838ff61d25c7b63; AWSALB=DzAZPuHY3geN44wcM8LFiAeEqplFHhdygYCZ8JHTHD+7Ty17IwexvUnY5ESP/iQyl2WU+noBvZejONPfQ2mNjna7gNI2E2u3gTQ0WtQIx130ks0lldgJ4SsOSTAe; AWSALBCORS=DzAZPuHY3geN44wcM8LFiAeEqplFHhdygYCZ8JHTHD+7Ty17IwexvUnY5ESP/iQyl2WU+noBvZejONPfQ2mNjna7gNI2E2u3gTQ0WtQIx130ks0lldgJ4SsOSTAe; search=6|1627955354655%7Crb%3DMiami-Beach%252C-FL%26rect%3D25.872806%252C-80.110191%252C25.747677%252C-80.17009%26disp%3Dmap%26mdm%3Dauto%26sort%3Ddays%26pt%3D%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%09%095924%09%09%09%09%09%09; _px3=df7e6fafaa304ea0de5956484794114c86dfc288786014c6d248dae11b5f6d9d:5b7RDqMZMk34P7/Hq4sWWuIsaDEabVd8IOS64DirpoED90E1iRU8CLIJHUcxm547vbvYZ5rCFjHB09gvZZRHEQ==:1000:V06EnVThG+i8Q3anFf89QLrsoHbFp6vcUZHX0wVcG5jS3SYecEvYy8pZwZx3/cHnX0qEqzG7NfaA4sJLXAnSAwPWeVMX1TK3GGZUnhoe7KhjDEZ6wSy6hEIf5ZlUSMecCgRHU3CwPeNR8H0tDc0Te6iUjZpbJj92JUAJDgpXEttZG8y5lKMxl1o4ia35tiTPKEMj7G1rL2pa8mJNAYoXlw=='
    cookie = SimpleCookie()
    cookie.load(cookie_string)

    cookies = {}

    for key, morsel in cookie.items():
        cookies[key] = morsel.value

    return cookies


def parse_new_url(url, page_number):
    url_parsed = urlparse(url)
    query_string = parse_qs(url_parsed.query)
    search_query_state = json.loads(query_string.get('searchQueryState')[0])
    search_query_state['pagination'] = {"currentPage": page_number}
    query_string.get('searchQueryState')[0] = search_query_state
    encoded_qs = urlencode(query_string, doseq=True)
    new_url = f"https://www.zillow.com/search/GetSearchPageState.htm?{encoded_qs}"
    return new_url
