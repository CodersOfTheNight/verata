from grazer.config import Mapping
from .fixtures import example_html



def test_0_depth(example_html):
    mapping = Mapping("title", "h1")
    result = mapping.parse(example_html)
    assert len(result) == 1
    assert result[0] == ("title", "Menu:", {})


def test_2_depth(example_html):
    mapping = Mapping("link", "ul/li/a")
    result = mapping.parse(example_html)
    assert result[0] == ("link", "Nested Link", {"href": "#"})


def test_4_depth(example_html):
    mapping = Mapping("link", "ul/li/ul/li[class=\"deep\"]/a")
    result = mapping.parse(example_html)
    assert result[0] == ("link", "Deepest one", {"href": "http://magic-link"})


def test_attr_selector(example_html):
    mapping = Mapping("link", "ul/li/ul/li[class=\"deep\"]/a.href")
    result = mapping.parse(example_html)
    assert result[0] == ("link", "http://magic-link", {"href": "http://magic-link"})
