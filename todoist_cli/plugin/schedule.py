from todoist_cli.plugin import Plugin
from todoist_cli.model.todoist import Todoist
from todoist_cli.model.calendar import Calendar

class Schedule(Plugin):
    def __init__(self, options):
        super(Schedule, self).__init__(options)
        self.todoist = Todoist()
        self.calendar = Calendar()

    def run(self):
        # TODO: get todoist items and register them in the calendar
        pass

# FIXME: (What is the best way to get instance?)
def plugin_instance(options):
    return Schedule(options)
