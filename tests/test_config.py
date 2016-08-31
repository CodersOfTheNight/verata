import pytest

from grazer.config import Config


def test_loading_existing():
    cfg = Config("tests/data/simple_config.yml")
    assert cfg is not None


def test_loading_nonexisting():
    with pytest.raises(FileNotFoundError):
        Config("tests/data/i-dont-exist.yml")
