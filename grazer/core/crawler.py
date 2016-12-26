import requests
import logging

from collections import deque
from functools import reduce
from copy import copy

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
    if link is None or len(link) == 0:
        return None

    if not link.startswith("http"):
        return ("/" if link[0] != "/" else "") + link

    if domain not in link:
        # External link to another domain
        logger.debug("Link {0} is not in {1} domain".format(link, domain))
        return None

    prefixes = ["https://", "http://", "://"]
    original_link = copy(link)
    link = reduce(lambda a, b: a.replace(b, ""), prefixes, link)
    if "/" in link:
        start, end = link.split("/", 1)
        return "/" + end
    else:
        return original_link


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
        logger.info("Doing authentification")
        auth = config.auth
        req = requests.Request(auth.method,
                               "{0}/{1}".format(root, auth.url),
                               data=auth.params)
        resp = session.send(req.prepare())
        logger.debug("Auth status code: {0}".format(resp.status_code))
        if resp.status_code >= 400:
            raise RuntimeError("Unable to do authentification")

    while len(queue) > 0:
        link = queue.popleft()
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
                logger.info("Scrapping: {0} using '{1}' page rules"
                            .format(link, page.name))
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

        logger.debug("Queued links: {0}".format(queue))
