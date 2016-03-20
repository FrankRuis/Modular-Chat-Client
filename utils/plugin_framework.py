from utils.logging import log


class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            log('\t\tSuccessfully imported {:s}', name)
            cls.plugins.append(cls)

    def get_plugins(cls, *args, **kwargs):
        return [p(*args, **kwargs) for p in cls.plugins]


class Command(metaclass=PluginMount):
    def __init__(self):
        self._enabled = True

    def help(self):
        """
        Return a string of command information
        """
        raise NotImplementedError('A command should implement the help method.')

    def call(self, *args, **kwargs):
        """
        Method is called when someone types the command name
        """
        raise NotImplementedError('A command should implement the call method.')

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, b):
        if b == self._enabled:
            return

        if b:
            log('Enabled the {:s} command.', self.args['name'])
        else:
            log('Disabled the {:s} command.', self.args['name'])
        self._enabled = b

    @staticmethod
    def get_commands(*args, **kwargs):
        return [{'class_name': p.__name__, 'class': p(*args, **kwargs), **p.args} for p in Command.plugins]

    @staticmethod
    def exists(command):
        return command in [p.args['name'] for p in Command.plugins]