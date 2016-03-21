import asyncio
import ssl
from core.connection import Connection
from utils.plugin_framework import Client, load_all_plugins

load_all_plugins()

ctx = ssl.create_default_context()
ctx.check_hostname = False
client = Client.get_clients()['ClientIRC']
c = client(Connection, 'kaascroissant')
c.connect('irc.freenode.org', port=6697, ssl=ctx)
asyncio.get_event_loop().run_forever()
