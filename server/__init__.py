import json
from .server import Server


with open('server/config.json', 'r') as configfile:
    config = json.load(configfile)

server = Server(config)
