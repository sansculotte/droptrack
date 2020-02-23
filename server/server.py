import atexit
import sys
import zmq


class Server(object):

    context = None

    def __init__(self, config={}):
        self.config = config
        self.context = zmq.Context.instance()
        webapp = self.context.socket(zmq.PULL)
        player = self.context.socket(zmq.PUB)
        webapp.bind(config['sockets']['webapp'])
        player.bind(config['sockets']['player'])
        self.webapp = webapp
        self.player = player
        self.topic = self.config.get('topic', 'soundfile')
        atexit.register(self.shutdown)

    def run(self):
        self.poller = zmq.Poller()
        self.poller.register(self.webapp, zmq.POLLIN)
        print('server listening on {}'.format(self.config['sockets']['webapp']))

        while True:
            try:
                socks = dict(self.poller.poll())

                if socks.get(self.webapp) == zmq.POLLIN:
                    message = self.webapp.recv_string()
                    print('frontend [{0!r}]'.format(message))
                    self.player.send_string('{} {}'.format(self.topic, message))
                    print('published on [{0}]'.format(self.topic))

            except KeyboardInterrupt:
                print(' signal caught ... exiting')
                sys.exit()

    def shutdown(self):
        self.poller.unregister(self.webapp)
        self.webapp.close()
        self.player.close()
        self.context.term()
