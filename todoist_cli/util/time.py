from datetime import datetime, timedelta
from tzlocal import get_localzone
from pytz import timezone, utc
from todoist_cli.util.config import Config

class Time(object):
    """
    Time utility

    :property:
    * self.yesterday_midnight
    * self.today_midnight
    * self.today_start
    * self.today_end

    If Config().settings['day_start'] == '09:30', the properties will be set as the following values.

    * self.yesterday_midnight   '00:00'
    * self.today_midnight       '24:00'
    * self.today_start          '09:30'
    * self.today_end            '24:00'
    """

    _instance = None
    _init = False

    def __init__(self):
        if Time._init:
            return None

        super(Time, self).__init__()

        self.local_timezone = timezone(str(get_localzone()))

        # NOTE: if day_start time in Todoist would be customizable, uncomment this.
        # day_start = datetime.strptime(
        #     '20000101 ' + Config().settings['day_start'],
        #     '%Y%m%d %H:%M'
        # )
        # today = datetime.now() - timedelta(hours=day_start.hour) - timedelta(minutes=day_start.minute)

        now = datetime.now()
        today_start = datetime.strptime(
            now.strftime('%Y%m%d ') + Config().settings['day_start'],
            '%Y%m%d %H:%M'
        )
        yesterday_midnight = datetime.strptime(
            now.strftime('%Y%m%d ') + '00:00',
            '%Y%m%d %H:%M'
        )

        self.yesterday_midnight = self.local_timezone.localize(yesterday_midnight)
        self.today_midnight = self.yesterday_midnight + timedelta(days=1)
        self.today_start = self.local_timezone.localize(today_start)
        self.today_end = self.today_midnight
        self.now = self.local_timezone.localize(now)

        Time._init = True

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def set_timezone(self, target_time, set_utc=False):
        """
        :param target_time: naive or aware time
        :return: aware time with local timezone

        Naive time is recognized as UTC and if set_utc is False it is converted to the time with local timezone.
        """
        if not (target_time.tzinfo and target_time.tzinfo.utcoffset(target_time)):
            target_time = utc.localize(target_time)

        return target_time.astimezone(utc if set_utc else self.local_timezone)

    def is_today(self, target_time):
        """
        :param target_time: the time to judge
        :return: (bool) whether target_time is today or not
        """

        target_time = self.set_timezone(target_time)

        return self.yesterday_midnight <= target_time < self.today_midnight
