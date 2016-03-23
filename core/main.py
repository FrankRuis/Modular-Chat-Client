import ssl
import sys

import asyncio
from PyQt4 import QtGui
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
        self.ui.actionConnect_2.triggered.connect(self.connect)

        client = Client.get_clients()['ClientIRC']
        self.client = client(Connection, self, 'kaascroissant')

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
