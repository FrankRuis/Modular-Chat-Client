from random import choice
from utils.plugin_framework import Command
from utils import hook

name = 'Test Plugin'


@hook.command('test')
class Test(Command):
    def help(self):
        print('Test')

    def call(self, *args, **kwargs):
        print(choice('Test'))
