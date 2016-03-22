from utils.plugin_framework import Handler
import asyncio


class Connection:
    def __init__(self, client, host, port, ssl=False):
        self.client = client
        self._connected = False
        self._ssl = ssl
        self._port = port
        self._host = host
        self._reader = None
        self._writer = None

    @asyncio.coroutine
    def connect(self):
        self._reader, self._writer = yield from asyncio.open_connection(self._host, self._port, ssl=self._ssl)
        self._connected = True
        self.client.on_connect()

        while self._connected:
            line = yield from self._reader.readline()
            if line:
                handlers = Handler.get_plugins(self.client)
                if handlers:
                    for handler in handlers:
                        handler.handle(line)
                else:
                    raise RuntimeError('There are no handlers to parse incoming messages.')
            else:
                self.disconnect()
                return

    def disconnect(self):
        self._writer.close()
        self._connected = False

    def send(self, msg):
        self._writer.write(msg)
