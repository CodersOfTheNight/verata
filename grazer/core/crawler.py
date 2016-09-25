import requests
import logging

from collections import deque

logger = logging.getLogger(__name__)


def get_session(cookies=None):
    session = requests.Session()
    if cookies:
        requests.utils.add_dict_to_cookiejar(session.cookies,
                                             cookies)
    return session


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
    proxies = config.proxies
    parser = config.parser
    reader = config.reader

    queue = deque(["{0}/{1}".format(root, start)])
    visited = []

    if config.has_auth():
        auth = config.auth
        req = requests.Request(auth.method,
                               "{0}/{1}".format(root, auth.url),
                               data=auth.params)
        resp = session.send(req.prepare())
        if resp.status_code > 400:
            raise RuntimeError("Unable to do authentification")

    while len(queue) > 0:
        link = queue.popleft()
        logger.info("Scrapping: {0}".format(link))
        try:
            data = reader.read_page(session, link, parser, headers, proxies)
            logger.debug("Retrieved data: {0}".format(data))
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

        logger.debug("Extracted links: {0}".format(links))

        for link in links:
            if link not in visited:
                queue.append(link)
