from utils.plugin_framework import Command
from utils.logging import log


def command(*variants, **kwargs):
    for variant in variants:
        if Command.exists(variant):
            log('\t\tThere already exists a command with the name {:s}.', variant)

    args = {'variants': [variant for variant in list(variants) if not Command.exists(variant)]}
    args.update(kwargs)

    def command_wrapper(cls):
        if not args['variants']:
            log('\t\tWarning: The {:s} command has no valid call variation.', cls.__name__)
        cls.args = args

        return cls

    return command_wrapper


def client_args(*args):
    def wrapper(cls):
        cls.args = args
        return cls

    return wrapper


def collect_triggers(cls):
    cls.triggers = {}
    for name, method in cls.__dict__.items():
        if hasattr(method, 'is_trigger') and method.is_trigger:
            for trig in method.triggers:
                if trig in cls.triggers:
                    cls.triggers[trig].append(method)
                else:
                    cls.triggers[trig] = [method]

    return cls


def trigger(*args, catch_all=False, catch_unknown=False):

    def trigger_wrapper(func):
        if catch_all:
            func.triggers = ('<catch_all>',)
        else:
            func.triggers = args
            if catch_unknown:
                func.triggers = ('<catch_unknown>', *func.triggers)
        func.is_trigger = True

        return func

    return trigger_wrapper
