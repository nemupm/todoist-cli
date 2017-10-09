from datetime import datetime
from todoist_cli.model import Model
from todoist.api import TodoistAPI
from todoist_cli.util.config import Config
from todoist_cli.util.time import Time
from re import match

class Todoist(Model):

    _instance = None
    _init = False

    def __init__(self):
        if Todoist._init:
            return None

        super(Todoist, self).__init__()

        self.api = TodoistAPI(Config().todoist['token'])
        self.api.sync()

        Todoist._init = True

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    @property
    def all_labels(self):
        labels = {}
        for label in self.api.labels.all():
            labels[label['id']] = label
        return labels

    @property
    def all_completed_items(self):
        return self.api.completed.get_all()['items']

    @property
    def all_today_items(self):
        """
        :return:
        (list of Item) all Todoist items including completed items due date of which are today.
        """

        today_items = []
        all_items = self.api.state['items']
        all_completed_items = self.all_completed_items
        all_completed_items_dict = {}

        for item in all_completed_items:
            all_completed_items_dict[item['id']] = item

        for item in all_items:
            # TODO: enable checked item
            if item['checked']:
                continue

            if not item['due_date_utc']:
                continue

            try:
                due = datetime.strptime(item['due_date_utc'], Item.TIME_FORMAT_DEFAULT)
            except:
                due = datetime.strptime(item['due_date_utc'], Item.TIME_FORMAT_API)

            if not Time().is_today(due):
                continue

            if item['id'] in all_completed_items_dict:
                item['completed_date'] = all_completed_items_dict[item['id']]['completed_date']

            today_items.append(Item(item))

        return today_items

class Item(Model):
    """
    @property content: task content
    @property checked: whether completed or not
    @property completed_date: (if checked is true) the date when the task completed
    """

    TIME_FORMAT_DEFAULT = "%a %d %b %Y %H:%M:%S +0000"
    TIME_FORMAT_API = "%Y-%m-%dT%H:%M"

    def __init__(self, item):
        super(Item, self).__init__()
        self.__item = item
        self.__all_day = item['all_day']
        self.__content = item['content']
        self.__day_order = item['day_order']
        self.__checked = item['checked']
        self.__completed_date = item['completed_date'] if item['checked'] else None
        self.__labels = item['labels']
        self.__due_date_utc = item['due_date_utc'] if item['due_date_utc'] else None

    @property
    def all_day(self):
        return self.__all_day

    @property
    def content(self):
        return self.__content

    @property
    def day_order(self):
        return self.__day_order

    @property
    def checked(self):
        return self.__checked

    @property
    def completed_date(self):
        return self.__completed_date

    @property
    def labels(self):
        return self.__labels

    @labels.setter
    def labels(self, values):
        self.__labels == values

    @property
    def due_date_utc(self):
        return self.__due_date_utc

    @due_date_utc.setter
    def due_date_utc(self, values):
        self.__due_date_utc = values

    @property
    def due_date_utc_datetime(self):
        try:
            due = datetime.strptime(self.__due_date_utc, Item.TIME_FORMAT_DEFAULT)
        except:
            due = datetime.strptime(self.__due_date_utc, Item.TIME_FORMAT_API)

        return Time().set_timezone(due, set_utc=True)

    @property
    def duration(self):
        duration = Config().settings['default_duration_minutes']

        for item_label_id in self.labels:
            if item_label_id not in Todoist().all_labels:
                continue
            label_name = Todoist().all_labels[item_label_id]['name']

            result = match(r'^-([0-9]+)min$', label_name)
            if result:
                duration = result.group(1)
                break

        return int(duration)

    def has_label(self, name):
        for item_label_id in self.labels:
            if item_label_id not in Todoist().all_labels:
                continue
            label_name = Todoist().all_labels[item_label_id]['name']
            if label_name == name:
                return True

        return False

    def attach_label(self, name):
        label_id_to_attach = None

        for label in Todoist().all_labels.values():
            if label['name'] == name:
                label_id_to_attach = label['id']
            if label_id_to_attach in self.labels:
                return
            break

        if not label_id_to_attach:
            new_label = Todoist().api.labels.add(name)
            Todoist().api.commit()
            label_id_to_attach = new_label['id']

        labels = self.labels
        labels.append(label_id_to_attach)
        self.__item.update(labels=labels)
        self.labels = labels

        Todoist().api.commit()

    def set_due_date(self, due_date):
        due_date_utc = Time().set_timezone(due_date, set_utc=True)
        due_date_utc_str = datetime.strftime(due_date_utc, self.TIME_FORMAT_API)

        self.__item.update(due_date_utc=due_date_utc_str)
        self.due_date_utc = due_date_utc_str

        Todoist().api.commit()

    def reset_due_date(self):
        self.__item.update(date_string="today")

        Todoist().api.commit()
