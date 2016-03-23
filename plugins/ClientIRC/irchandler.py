from utils.plugin_framework import Handler, log, Command
from utils.hook import trigger, collect_triggers
import re

action = '\1ACTION'


@collect_triggers
class IRCHandler(Handler):
    def handle(self, msg):
        message = IRCMessage(msg)
        self.trigger(message.command, self, message)

    @trigger('PING')
    def pong(self, message):
        self.client.send(('PONG ' + message.params))

    @trigger('PRIVMSG')
    def test(self, message):
        msg = message.message
        """
        if msg.startswith('!'):
            for command in Command.get_plugins():
                try:
                    cmd, params = msg.split(maxsplit=1)
                except ValueError:
                    cmd, params = msg, ''
                if cmd[1:] in command.args['variants']:
                    self.client.send('PRIVMSG {:s} :{:s}\r\n'
                                     .format(message.target, command.call(*params.split(command.args['split']))))
        """
        self.client.append_message(message.target, message.sender, msg)

    @trigger(catch_all=True)
    def catch_unknown(self, message):
        log(message.raw)


class IRCMessage:
    def __init__(self, raw):
        msg = raw.decode()
        self.raw = raw

        if msg.startswith(':'):
            self.prefix, self.command, self.params = msg.split(maxsplit=2)
        else:
            self.prefix = ''
            self.command, self.params = msg.split(maxsplit=1)

    @property
    def sender(self):
        if self.prefix:
            result = re.compile(r':(.*?)($|!)').match(self.prefix)
            return result.group(1) if result else None
        else:
            return ''

    @property
    def target(self):
        split = self.params.split()
        return split[0] if split else ''

    @property
    def message(self):
        split = self.params.split(maxsplit=1)
        if len(split) > 1:
            return split[1][1:].strip()
        else:
            return ''
