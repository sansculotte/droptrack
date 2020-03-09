import atexit
import sys
import zmq
from logging import getLogger, Formatter, StreamHandler
from logging.handlers import SysLogHandler
from .backlog import Backlog


class Server(object):
    """
    Broker between droptrack webapp and player
    Publishes urls, so a player subscribed to the soundfile channel
    gets realtime updates
    """
    context = None
    poller = None

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
        self.logger = self.setup_logging(config)
        atexit.register(self.shutdown)

    def setup_logging(self, config):
        """
        Logging comes in handy when server is daemonized
        """
        logging_config = config.get('logging')
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        level = 'debug'
        if logging_config:
            address = logging_config.get('address', '/dev/log')
            facility = logging_config.get('facility', 'LOG_SYSLOG')
            level = logging_config.get('level', level)
            handler = SysLogHandler(
                address=address,
                facility=SysLogHandler.__dict__[facility],
            )
        else:
            handler = StreamHandler(sys.stdout)

        handler.setFormatter(formatter)

        logger = getLogger(name='droptrack.server')
        logger.addHandler(handler)
        logger.setLevel(self.__log_level(level))
        return logger

    def __log_level(self, level):
        from logging import DEBUG, INFO, ERROR
        return {
            'debug': DEBUG,
            'info': INFO,
            'error': ERROR
        }[level]

    def run(self):
        self.poller = zmq.Poller()
        self.poller.register(self.webapp, zmq.POLLIN)
        self.poller.register(self.router, zmq.POLLIN)
        self.logger.info('listening on {}, {} and {}'.format(
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
                    self.logger.debug('frontend [{0!r}]'.format(message))
                    self.backlog.prepend(message)
                    self.player.send_string(
                        '{} {}'.format(self.topic, message)
                    )
                    self.logger.debug('published on [{0}]'.format(self.topic))

                # listen for requests from player
                if socks.get(self.router) == zmq.POLLIN:
                    command = self.router.recv_string()
                    self.logger.debug('router [{0}]'.format(command))
                    if command.startswith('backlog'):
                        try:
                            _, timestamp = command.split(' ')
                        except Exception as e:
                            self.logger.error(
                                'error unpacking router message {!r}'.format(e)
                            )
                            self.router.send_string('error')
                        else:
                            self.router.send_string('ok')
                            for entry in self.backlog.get_since(timestamp):
                                self.player.send_string(entry)
                                self.logger.debug(
                                    'sent on router: [{0}]'.format(entry)
                                )
                    else:
                        self.router.send_string('error')

            except KeyboardInterrupt:
                self.logger.info(' signal caught ... exiting')
                sys.exit()

    def shutdown(self):
        self.logger.info('shutting down')
        if self.poller:
            self.poller.unregister(self.webapp)
        self.webapp.close()
        self.player.close()
        self.router.close()
        self.context.term()
