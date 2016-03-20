from utils.plugin_framework import Command, load_all_plugins

load_all_plugins()

print(Command.get_commands())
