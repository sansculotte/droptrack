import requests
import shutil
import os, glob
from os import path
from urllib.parse import urlparse
from subprocess import run, CalledProcessError
from .player import PlayerError

import pandas as pd

class Store(object):

    def __init__(self, config):
        self.tracks = config.get('tracks', '/tmp')
        webapp = config.get('webapp')
        if webapp:
            self.webapps = [webapp]
        else:
            self.webapps = config.get('webapps', [])
        self.tracklog_filename = 'data/player_tracklog.csv'
        try:
            self.tracklog = pd.read_csv(self.tracklog_filename)
        except Exception as e:
            print('Could not load tracklog from file at {0}'.format(self.tracklog_filename))
            self.tracklog = pd.DataFrame(columns=['id', 'url', 'filename', 'filepath', 'length', 'fingerprint', 'hash'])

    def download(self, url):
        print('player.store.download from url {1} to self.tracks {0}'.format(self.tracks, url))
        components = urlparse(url)
        print('player.store.download url components {0}'.format(components))
        filename = None
        ytid = None
        trackinfo = self.tracklog[self.tracklog.url == url]
        if len(trackinfo) > 0:
            filename = str(trackinfo.filename.asobject[0])
            filepath = str(trackinfo.filepath.asobject[0])
            print('filename', filename)
            print('filepath', filepath)
            # found existing file, returning that skipping download
            if os.path.exists(filepath):
                return path.join(self.tracks, filename)
            trkid = int(trackinfo['id'])
        else:
            trkid = self.tracklog.index.max() + 1
            
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
        elif 'youtube.com' in components.netloc or 'youtu.be' in components.netloc:
            # command = ['youtube-dl', '-x', '-o', '{0}/%(title)s.%(ext)s'.format(self.tracks), '--audio-format', 'aac', url]
            # command = ['youtube-dl', '-x', '--audio-format', 'aac', '--get-filename', '-o', '{0}/%(title)s-%(id)s.%(ext)s'.format(self.tracks), url]
            command = ['youtube-dl', '-x', '--audio-format', 'mp3', '--audio-quality', '4', '-o', '{0}/%(title)s-%(id)s.%(ext)s'.format(self.tracks), url]
            ytid = components.query.split('v=')[-1]
            print('    ytid =', ytid)
            filename = '?'
        else:
            raise PlayerError('not soundcloud nor bandcamp')

        try:
            print('player.store running command {0}'.format(command))
            run(command, check=True)
        except CalledProcessError:
            print('failed to download from {}'.format(url))
        else:
            search_dir = self.tracks
            files = list(filter(os.path.isfile, glob.glob(search_dir + "/*")))
            print('files', files)
            if ytid is None:
                files.sort(key=lambda x: os.path.getmtime(x))
                print('files', files)
                # filename is most recent file in listing
                filename = path.basename(files[-1])
            else:
                # filename is the entry matching the youtube id
                # filename = files[files.index(ytid)]
                filename = list([_ for _ in files if ytid in _])
                print('ytid filename', filename)
                filename = filename[0]
                print('ytid filename', filename)
                filename = filename.split('/')[-1]
                print('ytid filename', filename)
                
            # print('filename', filename)
            row = [trkid, url, filename, self.tracks + filename, None, None, None]
            # print('    insert row', row)
            self.tracklog.loc[trkid] = row
            self.tracklog.to_csv(self.tracklog_filename, index=False)

            # return path.join(self.tracks, filename)
            return path.join(self.tracks, filename)

    def from_webapp(self, url):
        for w in self.webapps:
            print('player.store from_webapp url {0}, w {1}'.format(url, w))
            if url.startswith(w):
                return True
        return False

    def download_from_webapp(self, url, location):
        with requests.get(url, stream=True) as r:
            with open(location, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

    def queue_track(self, track_location):
        command = ['mocp', '--append', '--enqueue', '{0}'.format(track_location)]
        try:
            print('player.store.queue_track command {0}'.format(command))
            run(command, check=True)
        except CalledProcessError as e:
            print(e)
