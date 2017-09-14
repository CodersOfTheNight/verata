import logging

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def read_page(session, url, parser, headers=None, proxies=None):
    logger.debug("Reading url: {0} with parser: {1}".format(url, parser))
    raw = session.get(url, headers=headers, proxies=proxies).text
    return BeautifulSoup(raw, parser)
