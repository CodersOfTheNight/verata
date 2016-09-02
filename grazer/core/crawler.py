import requests
import re
from bs4 import BeautifulSoup


def get_session():
    return requests.Session()


def read_page(session, url):
    raw = session.get(url).text
    return BeautifulSoup(raw, "html.parser")


def extract_links(page):
    return [a.get("href") for a in page.find_all("a")]


def trim_link(link, root):
    return re.sub(root, "", link)


def create(config):
    root = config.root
    start = config.start_page
    pages = config.pages
    session = get_session()

    data = read_page("{0}/{1}".format(root, start))

    links = extract_links(data)
