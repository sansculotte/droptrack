from .collector import Collector
from .store import Store
from .player import PlayerError


config = {
    'server': 'tcp://127.0.0.1:5200',
    'tracks': './data/download'
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
    collector.run()
