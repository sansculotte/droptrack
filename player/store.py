import requests
import shutil
from os import path
from urllib.parse import urlparse
from subprocess import run, CalledProcessError
from .player import PlayerError


class Store(object):

    def __init__(self, config):
        self.tracks = config.get('tracks', '/tmp')
        webapp = config.get('webapp')
        if webapp:
            self.webapps = [webapp]
        else:
            self.webapps = config.get('webapps', [])

    def download(self, url):
        components = urlparse(url)
        if self.from_webapp(url):
            filename = path.basename(components.path)
            location = path.join(self.tracks, filename)
            command = ['curl', '-s', url, '--output', location]
            # this might also work in case curl is not available
            # self.download_from_webapp(url, location)
            # return location
        elif 'soundcloud.com' in components.netloc:
            command = ['soundscrape', '-p', self.tracks, url]
            filename = '?'
        elif 'bandcamp.com' in components.netloc:
            command = ['soundscrape', '-b', '-p', self.tracks, url]
            filename = '?'
        else:
            raise PlayerError('not soundcloud nor bandcamp')

        try:
            run(command, check=True)
        except CalledProcessError:
            print('failed to download from {}'.format(url))
        else:
            return path.join(self.tracks, filename)

    def from_webapp(self, url):
        for w in self.webapps:
            if url.startswith(w):
                return True
        return False

    def download_from_webapp(self, url, location):
        with requests.get(url, stream=True) as r:
            with open(location, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

    def queue_track(self, track_location):
        command = ['mocp', '-a', format(track_location)]
        try:
            run(command, check=True)
        except CalledProcessError as e:
            print(e)
