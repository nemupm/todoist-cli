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

        self.fixed_items = []

    def run(self):
        if self.options['now']:
            start_time = Time().now
        else:
            start_time = Time().today_start

        for item in self.todoist.all_today_items:
            if item.has_label(Config.LABEL_FIXED):
                self.fixed_items.append(item)
                continue
            elif item.has_label(Config.LABEL_SCHEDULED_BY_CLI):
                continue

            if item.all_day:
                item.attach_label(Config.LABEL_SCHEDULED_BY_CLI)
            else:
                item.attach_label(Config.LABEL_FIXED)
                self.fixed_items.append(item)

        for item in sorted(self.todoist.all_today_items, key=lambda x:x.day_order):
            start_time = self.set_due_date(item, start_time)

    def set_due_date(self, item, time):
        if item.has_label(Config.LABEL_FIXED):
            return time

        item.set_due_date(time)

        end_time = time + timedelta(minutes=item.duration)
        for fixed_item in sorted(self.fixed_items, key=lambda x:x.due_date_utc):
            if fixed_item.due_date_utc_datetime < time or fixed_item.due_date_utc_datetime >= end_time:
                continue

            end_time += timedelta(minutes=fixed_item.duration)

        # TODO: this should be removed in the future
        if end_time >= Time().today_midnight:
            end_time = Time().today_midnight - timedelta(minutes=1)

        return end_time

# FIXME: (What is the best way to get instance?)
def plugin_instance(options):
    return Schedule(options)
