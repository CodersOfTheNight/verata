import requests
from bs4 import BeautifulSoup


def get_session(cookies=None):
    session = requests.Session()
    if cookies:
        requests.utils.add_dict_to_cookiejar(session.cookies,
                                             cookies)
    return session


def read_page(session, url, parser, headers=None, proxies=None):
    raw = session.get(url, headers=headers, proxies=proxies).text
    return BeautifulSoup(raw, parser)
