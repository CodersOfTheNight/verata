import logging

from grazer.util import get_session

logger = logging.getLogger(__name__)


def scrape(link, cfg, mappings):
    reader = cfg.reader
    headers = cfg.headers
    proxies = cfg.proxies
    parser = cfg.parser
    session = get_session(cfg.cookies)

    data = reader.read_page(session, link, parser, headers, proxies)
    logger.debug("Retrieved data: {0}".format(data))

    parsed_data = [result
                   for mapping in mappings
                   for result in mapping.parse(data)]
    return list(parsed_data), link
