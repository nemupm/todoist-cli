from abc import ABCMeta, abstractmethod

class Plugin(object):
    __metaclass__ = ABCMeta

    def __init__(self, options):
        super(Plugin, self).__init__()
        self.options = options

    @abstractmethod
    def run(self):
        pass
