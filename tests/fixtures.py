from pytest import fixture
from bs4 import BeautifulSoup


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
                                <a href='http://magic-link'>Deepest one</a>
                            </li>
                        </ul>
                    </li>
                </ul>
            </body>
        </html>
    """
    return BeautifulSoup(html)
