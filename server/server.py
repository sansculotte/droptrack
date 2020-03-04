import atexit
import sys
import zmq
from .backlog import Backlog


class Server(object):
    """
    Broker between droptrack webapp and player
    Publishes urls, so a player subscribed to the soudnfile channel
    gets realtime updates
    """
    context = None

    def __init__(self, config=None):
        self.config = config or {}
        self.context = zmq.Context.instance()
        self.backlog = Backlog(config)
        webapp = self.context.socket(zmq.PULL)
        player = self.context.socket(zmq.PUB)
        router = self.context.socket(zmq.REP)
        webapp.bind(config['sockets']['webapp'])
        player.bind(config['sockets']['player'])
        router.bind(config['sockets']['router'])
        self.webapp = webapp
        self.player = player
        self.router = router
        self.topic = self.config.get('topic', 'soundfile')
        atexit.register(self.shutdown)

    def run(self):
        self.poller = zmq.Poller()
        self.poller.register(self.webapp, zmq.POLLIN)
        self.poller.register(self.router, zmq.POLLIN)
        print('listening on {}, {} and {}'.format(
            self.config['sockets']['webapp'],
            self.config['sockets']['player'],
            self.config['sockets']['router'],
        ))

        while True:
            try:
                socks = dict(self.poller.poll())
                # listen for urls pushed from webapp
                if socks.get(self.webapp) == zmq.POLLIN:
                    message = self.webapp.recv_string()
                    print('frontend [{0!r}]'.format(message))
                    self.backlog.prepend(message)
                    message_full = '{} {}'.format(self.topic, message)
                    self.player.send_string(
                        message_full
                    )
                    print('published on [{0}]'.format(message_full))

                # listen for requests from player
                if socks.get(self.router) == zmq.POLLIN:
                    command = self.router.recv_string()
                    print('router [{0}]'.format(command))
                    if command.startswith('backlog'):
                        try:
                            _, timestamp = command.split(' ')
                        except Exception as e:
                            print(
                                'error unpacking router message {!r}'.format(e)
                            )
                            self.router.send_string('error')
                        else:
                            self.router.send_string('ok')
                            for entry in self.backlog.get_since(timestamp):
                                message_full = '{} {}'.format(self.topic, entry)
                                self.player.send_string(message_full)
                                print('sent on router: [{0}]'.format(message_full))
                    else:
                        self.router.send_string('error')

            except KeyboardInterrupt:
                print(' signal caught ... exiting')
                sys.exit()

    def shutdown(self):
        self.poller.unregister(self.webapp)
        self.webapp.close()
        self.player.close()
        self.router.close()
        self.context.term()
