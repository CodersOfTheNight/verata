from pytest import fixture
from bs4 import BeautifulSoup

from grazer.config import Mapping


@fixture
def example_html():
    html = """
        <html>
            <body>
                <h1>Menu:</h1>
                <ul>
                    <li>
                        <a href=#>Nested Link</a>
                    </li>
                    <li>
                        <ul>
                            <li>
                                <a href=#>Incorrect</a>
                            </li>
                            <li class="deep">
                                <a href=#>Deepest one</a>
                            </li>
                        </ul>
                    </li>
                </ul>
            </body>
        </html>
    """
    return BeautifulSoup(html)


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
    assert result[0] == ("link", "Deepest one", {"href": "#"})
