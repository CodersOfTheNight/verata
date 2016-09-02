import requests
import re

from collections import deque
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

    queue = deque(["{0}/{1}".format(root, start)])
    visited = []

    while not queue.empty():
        link = queue.popleft()
        data = read_page(link)
        visited.append(link)

        for page in pages:
            if page.matches_link_pattern(link):
                for mapping in page.mappings:
                    yield mapping.parse(data)

        links = map(lambda x: root + x,
                    [trim_link(link, root)
                        for link in extract_links(data)])

        for link in links:
            if link not in visited:
                queue.append(link)
