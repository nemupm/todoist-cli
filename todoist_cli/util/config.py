import os
import configparser

class Config(object):

    _instance = None
    _init = False

    LABEL_SCHEDULED_BY_CLI = 'scheduled-by-cli'
    LABEL_FIXED = 'fixed'

    def __init__(self):
        if Config._init:
            return None

        super(Config, self).__init__()

        self.INIFILE = os.path.join(os.environ['HOME'], ".todoist_cli/config.ini")
        self.config = configparser.ConfigParser()

        try:
            self.config.read(self.INIFILE)
        except:
            print("%s does not exist." % self.INIFILE)
            raise

        Config._init = True

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    @property
    def todoist(self):
        return {
            'token': self.config.get('todoist', 'token')
        }

    @property
    def calendar(self):
        return {
            'key': self.config.get('calendar', 'key')
        }

    @property
    def settings(self):
        return {
            'day_start': self.config.get('settings', 'day_start', fallback="09:30"),
            'default_duration_minutes': self.config.get('settings', 'default_duration_minutes', fallback=60)
        }
