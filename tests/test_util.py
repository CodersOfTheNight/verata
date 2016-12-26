from grazer.util import time_convert, grouper


class TestTimeConvert(object):

    def test_seconds(self):
        assert time_convert("10s") == 10

    def test_minutes(self):
        assert time_convert("2m") == 120

    def test_hours(self):
        assert time_convert("3h") == 3 * 60 * 60


class TestGrouper(object):

    def test_simple_seq(self):
        seq = range(0, 10)
        result = list(grouper(2, seq))
        assert len(result) == 5
