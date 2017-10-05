from datetime import datetime, timedelta
from tzlocal import get_localzone
from pytz import timezone, utc
from todoist_cli.util.config import Config

class Time(object):

    _instance = None

    def __init__(self):
        super(Time, self).__init__()

        self.local_timezone = timezone(str(get_localzone()))

        day_start = datetime.strptime(
            '20000101 ' + Config().settings['day_start'],
            '%Y%m%d %H:%M'
        )
        # today = datetime.now() - timedelta(hours=day_start.hour) - timedelta(minutes=day_start.minute)
        today = datetime.now()
        today_start = datetime.strptime(
            today.strftime('%Y%m%d ') + Config().settings['day_start'],
            '%Y%m%d %H:%M'
        )
        self.today_start = self.local_timezone.localize(today_start)
        # self.today_end = self.today_start + timedelta(days=1)
        self.today_end = self.today_start + timedelta(days=1)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def is_today(self, target_time):
        if not (target_time.tzinfo and target_time.tzinfo.utcoffset(target_time)):
            target_time = utc.localize(target_time)

        target_time.astimezone(self.local_timezone)

        return self.today_start <= target_time < self.today_end
