import logging

from grazer.core import crawler
from grazer.config import Config

logging.basicConfig()


def test_scrape_python_org():
    cfg = Config("tests/data/python_org.yml")
    worker = crawler.create(cfg)
    (key, val), link = next(worker)
    assert key == "title"


def test_user_agent():
    session = crawler.get_session()
    resp = session.get("http://httpbin.org/user-agent", headers={"User-Agent": "test-agent"})
    assert resp.json()["user-agent"] == "test-agent"
