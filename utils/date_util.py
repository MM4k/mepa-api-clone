import datetime


class DateUtils:
    def get_yesterday_date(date):
        yesterday_date = datetime.datetime(date.year, date.month, date.day) - datetime.timedelta(1)

        return yesterday_date.date()

    def get_tomorrow_date(date):
        tomorrow_date = datetime.datetime(date.year, date.month, date.day) + datetime.timedelta(1)

        return tomorrow_date.date()
