from os import getcwd, path
from time import time
from .collector import Collector
from .store import Store
from .player import PlayerError


config = {
    'server': 'tcp://127.0.0.1:5200',
    'webapp': 'http://localhost:5000',
    'req': 'tcp://127.0.0.1:5210',
    'tracks': path.join(getcwd(), 'data/download'),
    'last_sync': './data/last_sync'
}


def handler(track_url):
    store = Store(config)
    try:
        location = store.download(track_url)
    except PlayerError as e:
        print(e)
    else:
        store.queue_track(location)


def main():
    collector = Collector(config)
    collector.register_handler(handler)
    if collector.request_backlog():
        collector.write_sync_time(time())
    else:
        print('backlog sync failed')

    collector.run()
