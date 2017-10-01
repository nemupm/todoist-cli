from datetime import datetime
from todoist_cli.model import Model
from todoist.api import TodoistAPI
from todoist_cli.util.config import Config

class Todoist(Model):
    def __init__(self):
        super(Todoist, self).__init__()
        self.api = TodoistAPI(Config().todoist['token'])
        self.api.sync()

    @property
    def all_completed_items(self):
        return self.api.completed.get_all()

    # FIXME: wrong items for JST
    @property
    def all_today_items(self):
        today_items = []
        today = datetime.utcnow().strftime("%a %d %b")

        print(today)
        for item in self.api.state['items']:
            due = item['due_date_utc']
            print(due)
            if due and due[:10] == today:
                today_items.append(item)

        return today_items
