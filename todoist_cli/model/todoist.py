from datetime import datetime
from todoist_cli.model import Model
from todoist.api import TodoistAPI
from todoist_cli.util.config import Config
from todoist_cli.util.time import Time

class Todoist(Model):

    _instance = None

    def __init__(self):
        super(Todoist, self).__init__()
        self.api = TodoistAPI(Config().todoist['token'])
        self.api.sync()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    @property
    def all_completed_items(self):
        return self.api.completed.get_all()

    @property
    def all_today_items(self):
        today_items = []

        for item in self.api.state['items']:
            due = item['due_date_utc']

            if not due:
                continue

            due = datetime.strptime(due, '%a %d %b %Y %H:%M:%S +0000')

            if Time().is_today(due):
                today_items.append(item)

        return today_items
