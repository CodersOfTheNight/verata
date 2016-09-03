import os
import pytest

from grazer.config import Config, Page, Mapping
from bs4 import BeautifulSoup


def test_loading_existing():
    cfg = Config("tests/data/simple_config.yml")
    assert cfg is not None


def test_loading_nonexisting():
    with pytest.raises(IOError):
        Config("tests/data/i-dont-exist.yml")


def test_info_fields():
    cfg = Config("tests/data/simple_config.yml")
    assert cfg.name == "Basic config"
    assert cfg.desc is not None


def test_secret_val():
    os.environ["SECRET"] = "5ecret"
    cfg = Config("tests/data/simple_config.yml")
    assert cfg.get_val("secret_val_1") == "5ecret"


def test_link_matcher():
    page = Page({"link_pattern": "%://google.com/#q=%"})
    result = page.matches_link_pattern("https://google.com/#q=test")
    assert result


def test_mapping():
    doc = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title"><b>The Dormouse's story</b></p>

    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>
    """

    root = BeautifulSoup(doc, "html.parser")
    m = Mapping("link1", "a[id=\"link1\"]")
    result = m.parse(root)
    expected = [("link1", root.find("a", {"id": "link1"}).text)]

    assert result == expected
