import pytest

from grazer.util import time_convert, grouper


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
