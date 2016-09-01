import os
import pytest

from grazer.config import Config, Page


def test_loading_existing():
    cfg = Config("tests/data/simple_config.yml")
    assert cfg is not None


def test_loading_nonexisting():
    with pytest.raises(FileNotFoundError):
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
