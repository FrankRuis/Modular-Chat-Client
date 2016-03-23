from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from utils.plugin_framework import Client
from utils.hook import client_args
from utils.logging import log


@client_args('nick', 'password', 'real_name', msg_size=512)
class ClientIRC(Client):
    def __init__(self, conn_cls, gui=None, nick='Anonymous', password=None, real_name=None):
        super().__init__(conn_cls, gui)
        self.nick = nick
        self._password = password
        self.real_name = nick if real_name is None else real_name

    def on_connect(self):
        if self._password is not None:
            self.send('PASS {:s}\r\n'.format(self._password))
        self.send('NICK {:s}\r\n'.format(self.nick))
        self.send('USER {:s} 0 * :{:s}\n\r'.format(self.nick, self.real_name))

    def join(self, channel):
        items = self.window.ui.treeWidget.findItems('irc.freenode.org', Qt.MatchExactly, 0)
        if items:
            item = QtGui.QTreeWidgetItem(items[0])
            item.setText(0, channel)
        self.send('JOIN {:s}\n\r'.format(channel))
        self.add_chat(channel)

    def leave(self, channel):
        self.send('PART {:s}\n\r'.format(channel))

    def append_message(self, target, sender, message):
        if target in self._chats:
            self._chats[target].append('<b>{:s}:</b> {:s}\n'.format(sender, message))
        else:
            log('Unknown target {:s}.', target)

    def send(self, msg):
        try:
            self._connection.send(msg)
        except ValueError as e:
            log('Error sending: {:s}', *e.args)
