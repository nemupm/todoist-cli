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

    if Config().settings['day_start'] == '09:30', the properties will be set as the following values.

    * self.yesterday_midnight   '00:00'
    * self.today_midnight       '24:00'
    * self.today_start          '09:30'
    * self.today_end            '24:00'
    """

    _instance = None

    def __init__(self):
        super(Time, self).__init__()

        self.local_timezone = timezone(str(get_localzone()))

        # NOTE: if day_start time in Todoist would be customizable, uncomment this.
        # day_start = datetime.strptime(
        #     '20000101 ' + Config().settings['day_start'],
        #     '%Y%m%d %H:%M'
        # )
        # today = datetime.now() - timedelta(hours=day_start.hour) - timedelta(minutes=day_start.minute)

        today = datetime.now()
        today_start = datetime.strptime(
            today.strftime('%Y%m%d ') + Config().settings['day_start'],
            '%Y%m%d %H:%M'
        )
        yesterday_midnight = datetime.strptime(
            today.strftime('%Y%m%d ') + '00:00',
            '%Y%m%d %H:%M'
        )

        self.yesterday_midnight = self.local_timezone.localize(yesterday_midnight)
        self.today_midnight = self.yesterday_midnight + timedelta(days=1)
        self.today_start = self.local_timezone.localize(today_start)
        self.today_end = self.today_midnight

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def is_today(self, target_time):
        """
        :return: (bool) whether target_time is today or not
        """

        if not (target_time.tzinfo and target_time.tzinfo.utcoffset(target_time)):
            target_time = utc.localize(target_time)

        target_time = target_time.astimezone(self.local_timezone)

        return self.today_start <= target_time < self.today_end
