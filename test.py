from utils.plugin_framework import Command
from utils.plugin_loader import load_all_plugins

load_all_plugins()

print(Command.get_commands())
