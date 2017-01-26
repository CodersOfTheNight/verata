from bs4 import BeautifulSoup


def read_page(session, url, parser, headers=None, proxies=None):
    raw = session.get(url, headers=headers, proxies=proxies).text
    return BeautifulSoup(raw, parser)
