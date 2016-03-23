import asyncio
import ssl
from core.connection import Connection
from utils.plugin_framework import Client, load_all_plugins

load_all_plugins()
ctx = ssl.create_default_context()
ctx.check_hostname = False
client = Client.get_clients()['ClientIRC']
c = client(Connection, 'kaascroissant', 'oauth:3r4c5ov57whhqsdyoicgthm2fyfsxq')
c.connect('irc.chat.twitch.tv', port=6667, ssl=False)
asyncio.get_event_loop().run_forever()
