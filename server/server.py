import atexit
import sys
import zmq


class Server(object):
    """
    Broker between droptrack webapp and player
    Publishes urls, so a player subscribed to the soudnfile channel
    gets realtime updates
    """
    context = None

    def __init__(self, config={}):
        self.config = config
        self.context = zmq.Context.instance()
        webapp = self.context.socket(zmq.PULL)
        player = self.context.socket(zmq.PUB)
        router = self.context.socket(zmq.ROUTER)
        webapp.bind(config['sockets']['webapp'])
        player.bind(config['sockets']['player'])
        self.webapp = webapp
        self.player = player
        self.topic = self.config.get('topic', 'soundfile')
        atexit.register(self.shutdown)

    def run(self):
        self.poller = zmq.Poller()
        self.poller.register(self.webapp, zmq.POLLIN)
        print('listening on {} and {}'.format(
            self.config['sockets']['webapp'],
            self.config['sockets']['player'],
        ))

        while True:
            try:
                socks = dict(self.poller.poll())

                # listen for urls pushed from webapp
                if socks.get(self.webapp) == zmq.POLLIN:
                    message = self.webapp.recv_string()
                    print('frontend [{0!r}]'.format(message))
                    self.player.send_string(
                        '{} {}'.format(self.topic, message)
                    )
                    print('published on [{0}]'.format(self.topic))

            except KeyboardInterrupt:
                print(' signal caught ... exiting')
                sys.exit()

    def shutdown(self):
        self.poller.unregister(self.webapp)
        self.webapp.close()
        self.player.close()
        self.context.term()
