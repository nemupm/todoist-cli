import os
import configparser

class Config(object):

    def __init__(self):
        super(Config, self).__init__()
        self.INIFILE = os.path.join(os.environ['HOME'], ".todoist_cli/config.ini")
        self.config = configparser.ConfigParser()

        try:
            self.config.read(self.INIFILE)
        except:
            print("%s does not exist." % self.INIFILE)
            raise

    @property
    def todoist(self):
        return {'token': self.config.get('todoist', 'token')}

    @property
    def calendar(self):
        return {'key': self.config.get('calendar', 'key')}
