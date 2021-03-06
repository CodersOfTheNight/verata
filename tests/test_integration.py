import logging

from grazer.core import crawler, scrapper
from grazer.config import Config

logging.basicConfig()


def test_crawl_python_org():
    cfg = Config("tests/data/python_org.yml")
    worker = crawler.create(cfg)
    data, link = next(worker)
    print(data)
    (key, text, attrs) = data[0]
    assert key == "title"


def test_scrape_python_org():
    cfg = Config("tests/data/python_org.yml")
    data = scrapper.fetch_page("http://python.org/blogs/", cfg)
    results = scrapper.scrape(data, cfg.mappings)
    print(results)
    (key, text, attrs) = results[0]
    assert key == "title"


def test_user_agent():
    session = crawler.get_session()
    resp = session.get("http://httpbin.org/user-agent", headers={"User-Agent": "test-agent"})
    assert resp.json()["user-agent"] == "test-agent"
