import requests
import logging

from six.moves import zip_longest
from copy import copy
from functools import reduce

logger = logging.getLogger("Util")


def time_convert(span):
    time_char = span[-1]
    val = span[:-1]
    if time_char == "s":
        return int(val)
    elif time_char == "m":
        return int(val) * 60
    elif time_char == "h":
        return int(val) * 3600
    else:
        raise RuntimeError("Unknown time format char: '{0}'".format(time_char))


def grouper(n, iterable):
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=None, *args)


def get_session(cookies=None):
    session = requests.Session()
    if cookies:
        requests.utils.add_dict_to_cookiejar(session.cookies,
                                             cookies)
    return session


def filter_empty(lst):
    def empty(x):
        return (x is None) or (len(x) == 0)

    return filter(lambda x: not empty(x), lst)


def extract_links(page, ignore_hashes=True):
    gen = [a.get("href") for a in page.find_all("a")]
    if ignore_hashes:
        result = map(lambda x: x.split("#")[0],
                     filter(lambda x: x is not None, gen))
    else:
        result = gen

    return list(set(map(lambda x: x.rstrip("/"), filter_empty(result))))


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
