from random import choice
from utils.plugin_framework import Command
from utils.hook import command


@command('choose')
class Choose(Command):
    def help(self):
        return 'Usage: choose option1, option2, ..., optionN. Chooses one of the provided options.'

    def call(self, *args, **kwargs):
        options = [option.strip() for option in ' '.join(args).split(',')]
        return 'I choose ' + choice(options)
