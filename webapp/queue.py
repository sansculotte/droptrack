from contextlib import contextmanager
import zmq # type: ignore

class Queue(object):

    def __init__(self, config):
        self.context = zmq.Context.instance()
        self.config = config

    @contextmanager
    def socket(self):
        try:
            socket = self.context.socket(zmq.PUSH)
            socket.connect(self.config['ROUTER'])
            yield socket
        finally:
            socket.close()

    def send(self, msg):
        with self.socket() as socket:
            socket.send_string(msg)

    def shutdown(self):
        self.context.term()
