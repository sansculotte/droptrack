from os import path
from urllib.parse import urlparse
from subprocess import run, CalledProcessError
from .player import PlayerError


class Store(object):

    def __init__(self, config):
        self.tracks = config.get('tracks', '/tmp')

    def download(self, url):
        components = urlparse(url)
        if 'soundcloud.com' in components.netloc:
            command = './venv/bin/soundscrape -p {} {}'.format(self.tracks, url)
        elif 'bandcamp.com' in components.netloc:
            command = './venv/bin/soundscrape -p {} {}'.format(self.tracks, url)
        else:
            raise PlayerError('not soundcloud nor bandcamp')

        try:
            run(command, check=True)
        except CalledProcessError:
            print('failed to download from {}'.format(url))
        else:
            return path.join(self.tracks, filename)

    def queue_track(self, track_location):
        command = 'mocp -a {}'.format(track_location)
        try:
            run(command, check=True)
        except CalledProcessError as e:
            print(e)
