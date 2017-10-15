from todoist_cli.plugin import Plugin
from todoist_cli.model.todoist import Todoist
from todoist_cli.model.calendar import Calendar
from todoist_cli.util.config import Config

class Reset(Plugin):

    def __init__(self, options):
        super(Reset, self).__init__(options)
        self.todoist = Todoist()
        self.calendar = Calendar()

    def run(self):
        for item in self.todoist.all_today_items:
            if not item.has_label(Config.LABEL_SCHEDULED_BY_CLI):
                continue

            item.reset_due_date()

        for item in self.todoist.all_expired_items:
            item.reset_due_date()

# FIXME: (What is the best way to get instance?)
def plugin_instance(options):
    return Reset(options)
