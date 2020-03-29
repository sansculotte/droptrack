import atexit
import sys
import zmq
from os import path
from time import time
from typing import Callable


class Collector(object):

    handlers = []
    req = None

    def __init__(self, config):
        self.last_sync = config.get('last_sync', './data/last_sync')
        self.topic = config.get('topic', 'soundfile')
        self.context = zmq.Context.instance()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(config['server'])
        self.socket.subscribe(self.topic)
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)

        req = config.get('req')
        if req:
            self.req = self.context.socket(zmq.REQ)
            self.req.setsockopt(zmq.LINGER, 0)
            self.req.connect(req)

        atexit.register(self.shutdown)

    def run(self):
        while True:
            try:
                socks = dict(self.poller.poll())
                if socks.get(self.socket) == zmq.POLLIN:
                    offset = len(self.topic) + 1
                    message = self.socket.recv_string()[offset:]
                    print('message {0}'.format(message))
                    self.write_sync_time()
                    for handler in self.handlers:
                        handler(message)

            except KeyboardInterrupt:
                print(' signal caught ... shutting down')
                sys.exit()

    def shutdown(self):
        self.poller.unregister(self.socket)
        self.socket.close()
        if self.req:
            self.poller.unregister(self.req)
            self.req.close()
        self.context.term()

    def register_handler(self, handler: Callable):
        self.handlers.append(handler)

    def unregister_handler(self, handler):
        # python should be able to do that, yes?
        self.handlers = [h for h in self.handlers if h is not handler]

    def request_backlog(self) -> bool:
        if self.req:
            timestamp = self.get_last_sync_time()
            if timestamp:
                self.req.send_string('backlog {}'.format(timestamp))
                self.poller.register(self.req, zmq.POLLIN)
                if self.poller.poll(1000):
                    r = self.req.recv_string()
                    return r == 'ok'
                else:
                    print('Timeout waiting for backlog')
        return False

    def get_last_sync_time(self) -> str:
        if path.exists(self.last_sync):
            with open(self.last_sync, 'r') as f:
                return f.read()
        return self.timestamp

    def write_sync_time(self):
        with open(self.last_sync, 'w') as f:
            f.write(self.timestamp)

    @property
    def timestamp(self) -> str:
        return '{:10.8}'.format(time() - 60 * 60 * 60 * 24)
