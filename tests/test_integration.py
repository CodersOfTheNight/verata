from grazer.core import crawler
from grazer.config import Config


def test_scrape_python_org():
    cfg = Config("tests/data/python_org.yml")
    worker = crawler.create(cfg)
    item = next(worker)
    assert item is not None
    assert "title" in item
