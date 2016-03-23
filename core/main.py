import ssl
import sys

import asyncio
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from quamash import QEventLoop

from core.connection import Connection
from core.mainwindow import Ui_MainWindow
from core.connectdialog import Ui_Dialog
from utils.plugin_framework import load_all_plugins, Client


class ConnectDialog(QtGui.QDialog, Ui_Dialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Chat Client')
        self.ui.actionConnect_2.triggered.connect(self.connect)
        self.ui.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested.connect(self.open_menu)

        client = Client.get_clients()['ClientIRC']
        self.client = client(Connection, self, 'rdpTestBot')

    def open_menu(self, position):
        indexes = self.ui.treeWidget.selectedIndexes()
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

            menu = QtGui.QMenu()
            if level == 0:
                join = menu.addAction(self.tr("Join channel"))
                disconnect = menu.addAction(self.tr("Disconnect"))
                join.triggered.connect(self.join)
            elif level == 1:
                leave = menu.addAction(self.tr("Leave channel"))
                leave.triggered.connect(lambda: self.leave(self.ui.treeWidget.itemFromIndex(indexes[0])))

            menu.exec_(self.ui.treeWidget.viewport().mapToGlobal(position))

    def leave(self, item):
        self.client.leave(item.text(0))
        self.ui.tabWidget.removeTab(self.ui.tabWidget.indexOf(self.client._chats[item.text(0)].parent()))
        item.parent().removeChild(item)

    def join(self):
        channel, ok = QtGui.QInputDialog.getText(self, 'Join channel', 'Channel name:')
        if ok:
            self.client.join(channel)

    def connect(self):
        dialog = ConnectDialog()
        if dialog.exec_():
            host, port, ssl = dialog.get_values()
            try:
                port = int(port)
                self.client.connect(host, port=port, ssl=ssl)
            except ValueError:
                QtGui.QMessageBox.about(self, 'Error','port should be an integer.')

if __name__ == '__main__':
    load_all_plugins()

    app = QtGui.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    #ctx = ssl.create_default_context()
    #ctx.check_hostname = False
    #client = Client.get_clients()['ClientIRC']
    #c = client(Connection, window, 'kaascroissant')
    #c.connect('irc.freenode.org', port=6667, ssl=False)

    with loop:
        loop.run_forever()

    sys.exit(app.exec_())
