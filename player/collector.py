import atexit
import sys
import zmq
from os import path
from time import time


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
        req = config.get('req')
        if req:
            self.req = self.context.socket(zmq.REQ)
            self.req.connect(req)

        atexit.register(self.shutdown)

    def run(self):
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)

        while True:
            try:
                socks = dict(self.poller.poll())
                if socks.get(self.socket) == zmq.POLLIN:
                    offset = len(self.topic) + 1
                    message = self.socket.recv_string()[offset:]
                    for handler in self.handlers:
                        handler(message)

            except KeyboardInterrupt:
                print(' signal caught ... shutting down')
                sys.exit()

    def shutdown(self):
        self.poller.unregister(self.socket)
        self.socket.close()
        if self.req:
            self.req.close()
        self.context.term()

    def register_handler(self, handler):
        self.handlers.append(handler)

    def unregister_handler(self, handler):
        # python should be able to do that, yes?
        self.handlers = [h for h in self.handlers if h is not handler]

    def request_backlog(self):
        if self.req:
            timestamp = self.get_last_sync_time()
            if timestamp:
                self.req.send_string('backlog {}'.format(timestamp))
                r = self.req.recv_string()
                return r == 'ok'

    def get_last_sync_time(self) -> str:
        if path.exists(self.last_sync):
            with open(self.last_sync, 'r') as f:
                return f.read()
        return '{:10.8}'.format(time() - 60 * 60 * 60 * 24)

    def write_sync_time(self, timestamp):
        with open(self.last_sync, 'w') as f:
            f.write('{:10.8f}'.format(timestamp))
