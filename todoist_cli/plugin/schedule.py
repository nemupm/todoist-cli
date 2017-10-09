from todoist_cli.plugin import Plugin
from todoist_cli.model.todoist import Todoist
from todoist_cli.model.calendar import Calendar
from todoist_cli.util.time import Time
from todoist_cli.util.config import Config
from datetime import timedelta

class Schedule(Plugin):

    def __init__(self, options):
        super(Schedule, self).__init__(options)
        self.todoist = Todoist()
        self.calendar = Calendar()

    def run(self):
        # TODO: get todoist items and register them in the calendar
        if self.options['now']:
            start_time = Time().now
        else:
            start_time = Time().today_start

        for item in sorted(self.todoist.all_today_items, key=lambda x:x.day_order):
            start_time = self.set_due_date(item, start_time)

    def set_due_date(self, item, time):
        # もし時間がかぶる予定があるなら、それだけ予定の終了予定時刻をずらす
        if item.has_label(Config.LABEL_FIXED):
            return time
        elif not item.has_label(Config.LABEL_SCHEDULED_BY_CLI) and not item.checked:
            if item.all_day:
                item.attach_label(Config.LABEL_SCHEDULED_BY_CLI)
            elif not item.all_day:
                item.attach_label(Config.LABEL_FIXED)

        item.set_due_date(time)

        return time + timedelta(minutes=item.duration)

# FIXME: (What is the best way to get instance?)
def plugin_instance(options):
    return Schedule(options)
