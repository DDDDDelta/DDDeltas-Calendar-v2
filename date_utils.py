# importing packages
from datetime import date, timedelta


class DateUtil:
    @staticmethod
    def get_today_date() -> date:
        """
        get today's date
        :return: date
        """
        return date.today()

    @staticmethod
    def get_delta_by_day(freq: int) -> timedelta:
        """
        get timedelta with number of days
        :param freq >= 0
        :return: timedelta
        """
        return timedelta(days=freq)

    @staticmethod
    def get_monday_from_today() -> date:
        """
        get the date of Monday of current week
        :return: date
        """
        return DateUtil.get_monday_from_date(DateUtil.get_today_date())

    @staticmethod
    def get_monday_from_date(given_date: date) -> date:
        """
        get the date of Monday of the week of the given date
        :param given_date: date
        :return: date
        """
        int_day = given_date.isoweekday()
        monday = 1
        time_delta = DateUtil.get_delta_by_day(int_day-monday)
        return given_date-time_delta

    @staticmethod
    def get_week_from_monday(monday: date) -> list[date]:
        """
        get the dates of the week in a list given a date
        :param monday: datetime.date
        :return: date[]
        """
        return [monday+DateUtil.get_delta_by_day(x) for x in range(7)]
