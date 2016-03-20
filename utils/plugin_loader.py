from importlib.util import find_spec
from importlib import import_module
from utils.logging import log
import os

PLUGIN_PACKAGE = 'plugins'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PLUGIN_FOLDER = os.path.join(BASE_DIR, PLUGIN_PACKAGE)
MAIN_MODULE = "__init__"


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
