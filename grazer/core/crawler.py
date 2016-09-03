import requests
import logging

from collections import deque
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def get_session(cookies=None):
    session = requests.Session()
    if cookies:
        for cookie in cookies:
            requests.utils.add_dict_to_cookiejar(session.cookies,
                                                 cookie)
    return session


def read_page(session, url, headers=None):
    raw = session.get(url, headers=headers).text
    return BeautifulSoup(raw, "html.parser")


def extract_links(page):
    return [a.get("href") for a in page.find_all("a")]


def trim_link(link, domain):
    if domain not in link:
        # External link to another domain
        return None

    link = link.replace("://", "")
    start, end = link.split("/", 1)
    return "/" + end


def create(config):
    root = config.root
    domain = config.domain
    start = config.start_page
    pages = config.pages
    session = get_session(config.cookies)
    headers = config.headers

    queue = deque(["{0}/{1}".format(root, start)])
    visited = []

    while len(queue) > 0:
        link = queue.popleft()
        logger.info("Scrapping: {0}".format(link))
        try:
            data = read_page(session, link, headers)
        except Exception as ex:
            logger.exception(ex)
            visited.append(link)
            continue

        visited.append(link)

        for page in pages:
            if page.matches_link_pattern(link):
                for mapping in page.mappings:
                    for result in mapping.parse(data):
                        yield result, link

        links = map(lambda x: root + x,
                    filter(lambda x: x is not None,
                           [trim_link(l, domain)
                            for l in extract_links(data)]))

        for link in links:
            if link not in visited:
                queue.append(link)
