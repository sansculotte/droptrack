from typing import Callable
import requests
import shutil
import os, glob
from os import path
from urllib.parse import urlparse
from subprocess import run, CalledProcessError
from .player import PlayerError

import pandas as pd
from soundscrape import soundscrape


def mocp_enqueue(location):
    command = ['mocp', '--append', '--enqueue', '{0}'.format(location)]
    try:
        print('player.store.queue_track command {0}'.format(command))
        run(command, check=True)
    except CalledProcessError as e:
        print(e)


def open_files(filenames):
    """
    replacement open_files for soundscrape
    """
    for location in filenames:
        mocp_enqueue(location)

# monkey patch sounscrape.open_file, with our callback to get to the
# filename
soundscrape.open_files = open_files


class Store(object):
    """
    Manage downloaded tracks
    """

    def __init__(self, config):
        self.tracks = config.tracks
        self.tracklog_filename = config.tracklog
        webapp = config.webapp
        if webapp:
            self.webapps = [webapp]
        else:
            self.webapps = config.webapps

        self.setup_tracklog()

    def setup_tracklog(self):
        """
        Tracklog keeps tabs on what we downloaded
        """
        try:
            self.tracklog = pd.read_csv(self.tracklog_filename)
        except Exception as e:
            print(
                'Could not load tracklog from file at {0}'.format(
                    self.tracklog_filename
                )
            )
            self.tracklog = pd.DataFrame(
                columns=['id', 'url', 'filename', 'filepath', 'length', 'fingerprint', 'hash']
            )

    def soundscrape_vargs(self, url: str) -> dict:
        return {
            'artist_url': url,
            'track': '',
            'keep': False,
            'open': True,
            'folders': False,
            'num_tracks': 1,
            'downloadable': False,
            'path': self.tracks,
        }

    def download(self, url: str, callback: Callable=open_files):
        print(
            'player.store.download from url {1} to self.tracks {0}'.format(
            self.tracks, url)
        )
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

        # download file from webapp
        if self.from_webapp(url):
            filename = path.basename(components.path)
            location = path.join(self.tracks, filename)
            command = ['curl', '-s', url, '--output', location]
            run(command, check=True)
            # this might also work in case curl is not available
            # self.download_from_webapp(url, location)
            mocp_enqueue(location)

        # soundscrape handlers
        elif 'soundcloud.com' in components.netloc:
            vargs = self.soundscrape_vargs(url)
            soundscrape.process_soundcloud(vargs)
        elif 'mixcloud.com' in components.netloc:
            vargs = self.soundscrape_vargs(url)
            soundscrape.process_mixcloud(vargs)
        elif 'audiomack.com' in components.netloc:
            vargs = self.soundscrape_vargs(url)
            soundscrape.process_audiomack(vargs)
        elif 'hive.co' in components.netloc:
            vargs = self.soundscrape_vargs(url)
            soundscrape.process_hive(vargs)
        elif 'musicbed.com'  in components.netloc:
            vargs = self.soundscrape_vargs(url)
            soundscrape.process_musicbed(vargs)

        # youtube
        elif 'youtube.com' in components.netloc or 'youtu.be' in components.netloc:
            # command = ['youtube-dl', '-x', '-o', '{0}/%(title)s.%(ext)s'.format(self.tracks), '--audio-format', 'aac', url]
            # command = ['youtube-dl', '-x', '--audio-format', 'aac', '--get-filename', '-o', '{0}/%(title)s-%(id)s.%(ext)s'.format(self.tracks), url]
            command = [
                'youtube-dl', '-x', '--audio-format', 'mp3',
                '--audio-quality', '4', '-o',
                '{0}/%(title)s-%(id)s.%(ext)s'.format(self.tracks),
                url
            ]
            ytid = components.query.split('v=')[-1]
            print('    ytid =', ytid)
        else:
            raise PlayerError('not soundscrape nor bandcamp nor youtube')

        # find most recent download
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
            filenames = list([f for f in files if ytid in f])
            if len(filenames) > 0:
                print('ytid filename', filename)
                filename = filenames[0]
                print('ytid filename', filename)
                filename = filename.split('/')[-1]
                print('ytid filename', filename)
            else:
                filename = 'N/A'
                print('could not generate filename')

        # maybe better not to hardcode track
        row = [trkid, url, filename, self.tracks + filename, None, None, None]
        self.tracklog.loc[trkid] = row
        self.tracklog.to_csv(self.tracklog_filename, index=False)

    def from_webapp(self, url):
        for app in self.webapps:
            print('player.store from_webapp url {0}, app {1}'.format(url, app))
            if url.startswith(app):
                return True
        return False

    def download_from_webapp(self, url, location):
        with requests.get(url, stream=True) as r:
            with open(location, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
