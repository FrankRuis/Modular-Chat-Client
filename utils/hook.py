from utils.plugin_framework import Command


def command(name, **kwargs):
    if Command.exists(name):
        raise ImportError('There already exists a command with the name {:s}.'.format(name))

    args = {'name': name}
    args.update(kwargs)

    def command_wrapper(cls):
        cls.args = args

        return cls

    return command_wrapper
