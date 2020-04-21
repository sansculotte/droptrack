from argparse import ArgumentParser
import json
import threading
from multiprocessing import Pool
from os import getcwd, path
from time import time
from .collector import Collector
from .store import Store
from .player import PlayerError


config = {
    'server': 'tcp://127.0.0.1:5200',
    'webapp': 'http://127.0.0.1:5000',
    'req': 'tcp://127.0.0.1:5210',
    'download_dir': path.join(getcwd(), 'data/download'),
    'last_sync': './data/last_sync',
    'tracklog': './data/player_tracklog.csv',
    'topic': 'soundfile',
}

if path.exists('./config.json'):
    with open('./config.json', 'r') as configfile:
        for key, value in json.load(configfile).items():
            config[key] = value


class Handler:
    """
    Callable class so we can set it up with config and run later.
    kind of currying actually.
    """
    def __init__(self, config):
        self.config = config

    def __call__(self, track_url):
        store = Store(self.config)
        try:
            store.download(track_url)
        except PlayerError as e:
            print(e)


def main():
    ap = ArgumentParser()
    ap.add_argument(
        '-s', '--server',
        dest='server', action='store', default=config.get('server'),
        help='url for server zmq subscription channel'
    )
    ap.add_argument(
        '-w', '--webapp',
        dest='webapp', action='store', default=config.get('webapp'),
        help='url for public webserver'
    )
    ap.add_argument(
        '-r', '--req',
        dest='req', action='store', default=config.get('req'),
        help='url for server zmq request channel (fetch backlog)'
    )
    ap.add_argument(
        '-d', '--download-dir',
        dest='tracks', action='store', default=config.get('download_dir'),
        help='path to local download directory'
    )
    ap.add_argument(
        '-t', '--topic',
        dest='topic', action='store', default=config.get('tracklog'),
        help='topic to subscribe to'
    )
    ap.add_argument(
        '--last-sync',
        dest='last_sync', action='store', default=config.get('last_sync'),
        help='path to last sync file holding the timestamp'
    )
    ap.add_argument(
        '--track-log',
        dest='tracklog', action='store', default=config.get('tracklog'),
        help='path to tracklog file'
    )
    ap.add_argument(
        '-n', '--no-sync',
        dest='sync_backlog', action='store_false',
        help='url for server zmq subscription channel'
    )
    args = ap.parse_args()

    collector = Collector(args)
    handler = Handler(args)
    collector.register_handler(handler)

    def backlog_req_func(*args, **kwargs):
        print('backlog request')
        if collector.request_backlog():
            collector.write_sync_time()
        else:
            print('backlog sync failed')

    if args.sync_backlog:
        thread = threading.Thread(target=backlog_req_func, args=(), kwargs={})
        thread.start()

    collector.run()
