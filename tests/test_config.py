import os
import pytest

from grazer.config import Config, Page, Mapping, Auth
from bs4 import BeautifulSoup


@pytest.fixture
def simple_config():
    return Config("tests/data/simple_config.yml")


@pytest.fixture
def simple_html():
    return """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title"><b>The Dormouse's story</b></p>

    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>
    """


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


def test_mapping(simple_html):
    root = BeautifulSoup(simple_html, "html.parser")
    m = Mapping("link1", "a[id=\"link1\"]")
    result = m.parse(root)
    expected = [("link1", root.find("a", {"id": "link1"}).text)]

    assert result == expected


class TestConfig(object):

    def test_text_repr(self, simple_config):
        assert (str(simple_config) ==
                "Basic config: So basic it is almost useless")

    def test_domain(self, simple_config):
        domain = simple_config.domain
        assert domain == "test.com"

    def test_unparsable_domain(self, simple_config):
        cfg = simple_config
        cfg._data["site_root"] = "spd://test.com"
        domain = cfg.domain
        assert domain == "spd://test.com"

    def test_empty_headers(self, simple_config):
        assert simple_config.headers is None

    def test_headers(self, simple_config):
        cfg = simple_config
        cfg._data["headers"] = {"test": "1"}
        assert cfg.headers == {"test": "1"}

    def test_empty_cookies(self, simple_config):
        assert simple_config.cookies is None

    def test_cookies(self, simple_config):
        cfg = simple_config
        cfg._data["cookies"] = {"test": "1"}
        assert cfg.cookies == {"test": "1"}

    def test_default_parser(self, simple_config):
        assert simple_config.parser == "html.parser"

    def test_custom_parser(self, simple_config):
        cfg = simple_config
        cfg._data["parser"] = "lxml"
        assert cfg.parser == "lxml"

    def test_default_proxies(self, simple_config):
        assert simple_config.proxies is None

    def test_custom_proxies(self, simple_config):
        cfg = simple_config
        cfg._data["proxies"] = ["http://10.10.10.10", "http://11.11.11.11"]
        assert cfg.proxies == ["http://10.10.10.10", "http://11.11.11.11"]

    def test_selecting_tag_from_list(self, simple_html):
        root = BeautifulSoup(simple_html, "html.parser")
        m = Mapping("link", "a{2}")
        result = m.parse(root)
        expected = [("link", root.findAll("a")[2].text)]

        assert result == expected


class TestAuth(object):

    def test_default_method(self):
        auth = Auth({})
        assert auth.method == "POST"

    def test_custom_method(self):
        auth = Auth({"method": "PATCH"})
        assert auth.method == "PATCH"

    def test_url(self):
        auth = Auth({"url": "/login"})
        assert auth.url == "/login"

    def test_params(self):
        auth = Auth({"params": {"user": "test_user",
                                "password": "test_passw"}
                     })
        assert auth.params["user"] == "test_user"
        assert auth.params["password"] == "test_passw"
