from random import randint
from utils.plugin_framework import Command
from utils.hook import command


@command('roll', 'diceroll')
class Dice(Command):
    def help(self):
        return 'Usage: roll: Roll a 6 sided die. roll n: Roll a number between 0 and n.'

    def call(self, *args, **kwargs):
        if len(args) > 0 and args[0].isdigit() and int(args[0]) > 0:
            return 'Rolled {:d}.'.format(randint(0, int(args[0])))
        else:
            return 'Rolled {:d}.'.format(randint(1, 6))
