import logging

logger = logging.getLogger(__name__)


def scrape(link, data, mapping):
    parsed_data = [result
                   for result in mapping.parse(data)]
    return list(parsed_data), link
