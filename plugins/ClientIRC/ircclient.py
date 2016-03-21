from utils.plugin_framework import Client
from utils.hook import client_args


@client_args('nick', 'password', 'real_name')
class ClientIRC(Client):
    def __init__(self, conn_cls, nick='Anonymous', password=None, real_name=None):
        super().__init__(conn_cls)
        self._nick = nick
        self._password = password
        self._real_name = nick if real_name is None else real_name

    def on_connect(self):
        if self._password is not None:
            self._connection.send('PASS {:s}\n\r'.format(self._password).encode())
        self._connection.send('NICK {:s}\n\r'.format(self._nick).encode())
        self._connection.send('USER {:s} 0 * :{:s}\n\r'.format(self._nick, self._real_name).encode())
        self._connection.send('JOIN {:s}\n\r'.format('#kekkels').encode())

    def send(self, msg):
        self._connection.send(msg)
