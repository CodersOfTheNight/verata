from grazer.core import crawler
from bs4 import BeautifulSoup


def test_extract_links():
    text = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title"><b>The Dormouse's story</b></p>

    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>
    </body>
    </html>
    """

    bs = BeautifulSoup(text, "html.parser")

    links = crawler.extract_links(bs)
    expected = ["http://example.com/elsie",
                "http://example.com/lacie",
                "http://example.com/tillie"]

    assert set(links) == set(expected)


def test_link_trimmer():
    result = crawler.trim_link("http://example.com/lacie", "http://example.com")
    assert result == "/lacie"


def test_trim_link_without_trailing_slash():
    result = crawler.trim_link("http://example.com", "http://example.com")
    assert result == "http://example.com"
