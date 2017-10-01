import importlib

class Client(object):

    def __init__(self, plugin, options):
        super(Client, self).__init__()

        # load plugin
        self.plugin = importlib.import_module("todoist_cli.plugin." + plugin).plugin_instance(options)

    def run(self):
        self.plugin.run()
