from random import randint
from utils.plugin_framework import Command
from utils import hook


@hook.command('roll')
class Dice(Command):
    def help(self):
        print('Usage:\n'
              'roll: Roll a 6 sided die.\n'
              'roll n: Roll n 6 sided dice and sum the result.')

    def call(self, *args, **kwargs):
        if len(args) > 0 and args[0] > 1:
            total = 0
            for _ in range(args[0]):
                total += randint(1, 6)
            print('Rolled {:d} in {:d} rolls.'.format(total, args[0]))
        else:
            print('Rolled {:d}.'.format(randint(1, 6)))
