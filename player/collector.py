import atexit
import sys
import zmq


class Collector(object):

    handlers = []

    def __init__(self, config):
        self.topic = config.get('topic', 'soundfile')
        self.context = zmq.Context.instance()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(config['server'])
        self.socket.subscribe(self.topic)
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
        self.context.term()

    def register_handler(self, handler):
        self.handlers.append(handler)

    def unregister_handler(self, handler):
        # python should be able to do that, yes?
        self.handlers = [h for h in self.handlers if h is not handler]
