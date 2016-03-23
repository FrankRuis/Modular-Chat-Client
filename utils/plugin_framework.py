from PyQt4 import QtGui, QtCore
from importlib.util import find_spec
from importlib import import_module

import asyncio

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
    def __init__(self, enabled=True):
        self._enabled = enabled

    def help(self):
        """
        Return a string of command information
        """
        return 'This command has no information.'

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
    def get_commands():
        return {p.__name__: p for p in Command.plugins}

    @staticmethod
    def exists(command):
        for p in Command.plugins:
            if hasattr(p, 'args'):
                if 'variants' in p.args and command in p.args['variants']:
                    return True
        return False


class Handler(metaclass=PluginMount):
    def __init__(self, client):
        self.client = client

    def handle(self, msg):
        raise NotImplementedError

    def trigger(self, trig, *args, **kwargs):
        if '<catch_all>' in self.triggers:
            for method in self.triggers['<catch_all>']:
                method(*args, **kwargs)

        if trig in self.triggers:
            for method in self.triggers[trig]:
                method(*args, **kwargs)
        elif '<catch_unknown>' in self.triggers:
            for method in self.triggers['<catch_unknown>']:
                method(*args, **kwargs)
        elif not '<catch_all>' in self.triggers:
            log('Unknown trigger {0}.', trig)


class Client(metaclass=PluginMount):
    args = ()

    def __init__(self, conn_cls, gui):
        self.window = gui
        self._con_cls = conn_cls
        self._connection = None
        self._chats = {}

    def connect(self, host, **kwargs):
        self._connection = self._con_cls(self, host, **kwargs)
        item = QtGui.QTreeWidgetItem(self.window.ui.treeWidget)
        item.setText(0, host)

        return asyncio.Task(self._connection.connect())

    def add_chat(self, name):
        tab = QtGui.QWidget()
        tab.setObjectName(name)
        vertical_layout = QtGui.QVBoxLayout(tab)
        vertical_layout.setMargin(11)
        vertical_layout.setMargin(6)
        text_edit = QtGui.QTextEdit(tab)
        self._chats[name] = text_edit
        text_edit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        vertical_layout.addWidget(text_edit)
        line_edit = QtGui.QLineEdit(tab)
        vertical_layout.addWidget(line_edit)
        self.window.ui.tabWidget.addTab(tab, name)

    def on_connect(self):
        raise NotImplementedError

    @staticmethod
    def get_clients():
        return {client.__name__: client for client in Client.plugins}


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
    log('Done loading plugins')
