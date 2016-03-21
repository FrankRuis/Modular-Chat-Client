from random import randint
from utils.plugin_framework import Command
from utils.hook import command


@command('roll', 'diceroll')
class Dice(Command):
    def help(self):
        return 'Usage: roll: Roll a 6 sided die. roll n: Roll n 6 sided dice and sum the result.'

    def call(self, *args, **kwargs):
        if len(args) > 0 and args[0].isdigit() and int(args[0]) > 1:
            total = 0
            for _ in range(int(args[0])):
                total += randint(1, 6)
            return 'Rolled {:d} in {:s} rolls.'.format(total, args[0])
        else:
            return 'Rolled {:d}.'.format(randint(1, 6))
