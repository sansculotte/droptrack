from time import time
from os import path

class Backlog(object):

    def __init__(self, config=None):
        self.__config = config or {}
        self.__file = config.get('backlog', './data/backlog.txt')

    def prepend(self, message, timestamp=None):
        timestamp = timestamp or time()
        # TODO filelock
        # TODO rotate
        if path.exists(self.__file):
            with open(self.__file, 'r+') as f:
                old = f.read()
                f.seek(0)
                f.write('{:10.8f}-{}\n{}'.format(timestamp, message, old))
        else:
            with open(self.__file, 'w') as f:
                f.write('{:10.8f}-{}'.format(timestamp, message))

    def get_since(self, timestamp: str):
        with open(self.__file, 'r') as file:
            for line in file:
                t, url = line.rstrip('\n').split('-', 1)
                if t < timestamp:
                    yield url
                else:
                    break
