from datetime import date

import pytest

from utils.date_util import DateUtils


@pytest.mark.django_db
class TestDateUtils:
    def setup_method(self):
        self.date_test = date(year=2022, month=1, day=15)

        self.yesterday_date = date(year=2022, month=1, day=14)
        self.tomorrow_date = date(year=2022, month=1, day=16)

    def test_get_yesterday_date(self):
        date = DateUtils.get_yesterday_date(self.date_test)

        assert date == self.yesterday_date

    def test_get_tomorrow_date(self):
        date = DateUtils.get_tomorrow_date(self.date_test)

        assert date == self.tomorrow_date
