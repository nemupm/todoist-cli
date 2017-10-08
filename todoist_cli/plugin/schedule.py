from todoist_cli.plugin import Plugin
from todoist_cli.model.todoist import Todoist
from todoist_cli.model.calendar import Calendar
from todoist_cli.util.time import Time

class Schedule(Plugin):

    def __init__(self, options):
        super(Schedule, self).__init__(options)
        self.todoist = Todoist()
        self.calendar = Calendar()

    def run(self):
        # TODO: get todoist items and register them in the calendar
        start_time = Time().today_start
        for item in self.todoist.all_today_items:
            # print(item)
            print(item.content)
            if not item.all_day:
                print(item.due_date_utc)
            print(item.duration)
            start_time = self.set_due_date(item, start_time)

    def set_due_date(self, item, time):
        # もし時間がかぶる予定があるなら、それだけ予定の終了予定時刻をずらす
        if item.all_day and not item.checked:
            print('test')
            item.attach_label('scheduled_by_cli')

# FIXME: (What is the best way to get instance?)
def plugin_instance(options):
    return Schedule(options)
