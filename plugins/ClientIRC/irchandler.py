from utils.plugin_framework import Handler, log, Command
from utils.hook import trigger, collect_triggers


@collect_triggers
class IRCHandler(Handler):
    def handle(self, msg):
        parts = msg.decode().split()
        if len(parts) > 1:
            if parts[0].startswith(':'):
                self.trigger(parts[1], self, parts[1:])
            else:
                self.trigger(parts[0], self, parts)

    @trigger('PING')
    def pong(self, parts):
        self.client.send(('PONG ' + ' '.join(parts[1:])).encode())

    @trigger('PRIVMSG')
    def test(self, parts):
        msg = ' '.join(parts[2:])[1:]
        if msg.startswith('!'):
            for command in Command.get_plugins():
                params = msg.split()
                if params[0][1:] in command.args['variants']:
                    if parts[1] == 'kaascroissant':
                        parts[1] = '#kekkels'
                    self.client.send('PRIVMSG {:s} :{:s}\r\n'.format(parts[1], command.call(*params[1:])).encode())

        log(' '.join(parts))

    @trigger(catch_unknown=True)
    def catch_all(self, parts):
        log(' '.join(parts))
