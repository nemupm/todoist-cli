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
        for item in self.todoist.all_today_items:
            print(item)
            # print(item['content'])
        pass

        # for

# FIXME: (What is the best way to get instance?)
def plugin_instance(options):
    return Schedule(options)
