from importlib.util import find_spec
from importlib import import_module
from utils.logging import log
import os

PLUGIN_PACKAGE = 'plugins'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PLUGIN_FOLDER = os.path.join(BASE_DIR, PLUGIN_PACKAGE)
MAIN_MODULE = "__init__"


class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            log('\t\tSuccessfully imported {:s}', name)
            cls.plugins.append(cls)

    def get_plugins(cls, *args, **kwargs):
        return [p(*args, **kwargs) for p in cls.plugins]


class Command(metaclass=PluginMount):
    def __init__(self):
        self._enabled = True

    def help(self):
        """
        Return a string of command information
        """
        raise NotImplementedError('A command should implement the help method.')

    def call(self, *args, **kwargs):
        """
        Method is called when someone types the command name
        """
        raise NotImplementedError('A command should implement the call method.')

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, b):
        if b == self._enabled:
            return

        if b:
            log('Enabled the {:s} command.', self.args['name'])
        else:
            log('Disabled the {:s} command.', self.args['name'])
        self._enabled = b

    @staticmethod
    def get_commands(*args, **kwargs):
        return {p.args['name']: p(*args, **kwargs) for p in Command.plugins}

    @staticmethod
    def exists(command):
        return command in [p.args['name'] for p in Command.plugins]


def find_plugins():
    plugins = []
    possible_plugins = os.listdir(PLUGIN_FOLDER)

    for p in possible_plugins:
        location = os.path.join(PLUGIN_FOLDER, p)
        if not os.path.isdir(location) or not MAIN_MODULE + ".py" in os.listdir(location):
            continue

        info = find_spec('{:s}.{:s}'.format(PLUGIN_PACKAGE, p))
        plugins.append({"name": p, "spec": info})

    return plugins


def load_plugin(plugin):
    log('\tLoading {:s}:', plugin['spec'].name)
    try:
        return import_module(plugin['spec'].name)
    except ImportError as error:
        log('\t\tImport failed: {:s}', *error.args)


def load_all_plugins():
    log('Loading plugins:')
    for plugin in find_plugins():
        load_plugin(plugin)
