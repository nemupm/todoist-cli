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
        return self.api.completed.get_all()['items']

    @property
    def all_today_items(self):
        today_items = []
        all_completed_items = self.all_completed_items
        all_completed_items_dict = {}

        for item in all_completed_items:
            all_completed_items_dict[item['id']] = item

        for item in self.api.state['items']:
            due = item['due_date_utc']

            if not due:
                continue

            due = datetime.strptime(due, '%a %d %b %Y %H:%M:%S +0000')

            if not Time().is_today(due):
                continue

            if item['id'] in all_completed_items_dict:
                item['completed_date'] = all_completed_items_dict['completed_date']

            today_items.append(item)

        return today_items
