import os
import re
import yaml

from functools import reduce
from jinja2 import Template


def pattern_to_regex(patt):
    lang = {"%": ".*?",
            "*": "."}
    patt = reduce(lambda a, b: a.replace(b[0], b[1]), lang.items(), patt)
    return re.compile(patt)


class Page(object):

    """
    Represents config subset for concrete page
    """

    def __init__(self, cfg):
        self._data = cfg
        self.matcher = pattern_to_regex(cfg["link_pattern"])

    def matches_link_pattern(self, url):
        return self.matcher.search(url) is not None


class Mapping(object):

    """
    Maps concete text from html element to column
    """

    def __init__(self, key, pattern):
        self.path = [self.create_node(part)
                     for part in pattern.split("/")]

    def create_node(self, data):
        patt = re.compile(r"(?P<tag>\w+)(?P<query>\[(?P<attr>\w+)=(\"|\')(?P<val>.+?)(\"|\')\])?")

        m = patt.match(data)
        tag = m.group("tag")

        if m.group("query"):
            q = {m.group("attr"): m.group("val")}
        else:
            q = None

        def node(root):
            return root.find(tag, q)

        return node

    def parse(self, root):
        return reduce(lambda context, fn: fn(context), self.path, root).text


class Config(object):

    """
    Class which handles config related stuff
    """

    def __init__(self, f):
        with open(f, "r") as f:
            self._data = self._render(f)

    def __repr__(self):
        return "{0}: {1}".format(self.name, self.desc)

    def _render(self, f):
        tmpl = Template(f.read())

        def env_get():
            return dict(os.environ)

        return yaml.load(tmpl.render(**env_get()))

    @property
    def name(self):
        return self._data["name"]

    @property
    def desc(self):
        return self._data["description"]

    @property
    def root(self):
        return self._data["site_root"]

    @property
    def start_page(self):
        return self._data["start_page"]

    @property
    def pages(self):
        return [Page(cfg)
                for cfg in self._data["pages"]]

    def get_val(self, key):
        return self._data["vars"][key]
