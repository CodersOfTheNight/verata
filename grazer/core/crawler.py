import requests
import logging

from collections import deque
from .scrapper import scrape

from grazer.util import trim_link, extract_links

logger = logging.getLogger(__name__)


def create(config):
    root = config.root
    domain = config.domain
    start = config.start_page
    pages = config.pages
    reader = config.reader
    session = reader.get_session(config.cookies)
    headers = config.headers
    proxies = config.proxies
    parser = config.parser

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

        relevant_pages = [page
                          for page in pages
                          if page.matches_link_pattern(link)]

        for page in relevant_pages:
            logger.info("Scrapping: {0} using '{1}' page rules"
                        .format(link, page.name))

            yield scrape(data, page.mappings), link

        links = map(lambda x: root + x,
                    filter(lambda x: x is not None,
                           [trim_link(l, domain)
                            for l in extract_links(data,
                                                   config.ignore_hashes
                                                   )
                            ]))

        for l in set([l
                      for l in links
                      if l not in visited]):
            queue.append(l)

        logger.debug("Queued links: {0}".format(queue))
