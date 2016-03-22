from utils.plugin_framework import Command
from utils.hook import command
import requests


@command('strawpoll', 'poll', split=',')
class Strawpoll(Command):
    def help(self):
        return 'Usage: strawpoll title, option1, option2, ..., optionN.'

    def call(self, *args, **kwargs):
        if len(args) > 2:

            request = requests.post("https://strawpoll.me/api/v2/polls",
                                    headers={'content-type': 'application/json'},
                                    json={'title': args[0], 'options': [option.strip() for option in args[1:]]})

            response = request.json()
            if 'id' in response:
                return 'https://www.strawpoll.me/' + str(response['id'])
        else:
            return 'Please provide at least 2 options and a title.'
