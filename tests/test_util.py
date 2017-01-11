import pytest

from grazer.util import time_convert, grouper, extract_links, trim_link
from .fixtures import example_html


class TestTimeConvert(object):

    def test_seconds(self):
        assert time_convert("10s") == 10

    def test_minutes(self):
        assert time_convert("2m") == 120

    def test_hours(self):
        assert time_convert("3h") == 3 * 60 * 60

    def test_unknown(self):
        with pytest.raises(RuntimeError):
            time_convert("5u")


class TestGrouper(object):

    def test_simple_seq(self):
        seq = range(0, 10)
        result = list(grouper(2, seq))
        assert len(result) == 5

    def test_odd_seq(self):
        seq = range(0, 10)
        result = list(grouper(3, seq))
        assert len(result) == 4
        assert result[-1] == (9, None, None)


class TestLinkExtract(object):

    def test_extract_wo_hashes(self, example_html):
        result = extract_links(example_html, ignore_hashes=True)
        assert len(result) == 1
        assert result[0] == "http://magic-link"

    def test_extract_w_hashes(self, example_html):
        result = extract_links(example_html, ignore_hashes=False)
        assert "http://magic-link/#/with-hash" in result

    def test_trim_link_absolute(self):
        link = "http://magic-link.dev/something-good"
        result = trim_link(link, "magic-link.dev")
        assert result == "/something-good"

    def test_trim_link_relative(self):
        link = "/something-good"
        result = trim_link(link, "magic-link.dev")
        assert result == "/something-good"

    def test_trim_link_external_domain(self):
        link = "http://google.com"
        result = trim_link(link, "magic-link.dev")
        assert result is None
