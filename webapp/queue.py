import zmq

class Queue(object):

    def __init__(self, config):
        self.context = zmq.Context.instance()
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.connect(config['ROUTER'])

    def send(self, msg):
        self.socket.send_string(msg)

    def shutdown(self):
        self.socket.close()
        self.context.term()
