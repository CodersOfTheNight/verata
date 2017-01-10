import logging

from grazer.util import get_session

logger = logging.getLogger(__name__)


def fetch_page(link, cfg):
    reader = cfg.reader
    headers = cfg.headers
    proxies = cfg.proxies
    parser = cfg.parser
    session = get_session(cfg.cookies)

    return reader.read_page(session, link, parser, headers, proxies)


def scrape(data, mappings):
    logger.debug("Retrieved data: {0}".format(data))

    parsed_data = [result
                   for mapping in mappings
                   for result in mapping.parse(data)]
    return list(parsed_data)
