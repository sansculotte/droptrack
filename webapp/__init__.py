# -*- coding: utf-8 -*-
import string, random
from pprint import pformat
import atexit
from logging import Formatter
from logging.handlers import SysLogHandler
import os
from flask import (
    Flask,
    current_app,
    request,
    session,
    render_template,
    make_response,
)
from .queue import Queue
from .api import api
from .api_smp import api_smp
# from .filesys import walkdirlist

dt_session_default = 'zniz'

############################################################
# data

try:
    APP_ENV = os.environ['APP_ENV']
except KeyError:
    APP_ENV = 'config.Config'

def root():
    return render_template('main.html')

def setup_routes(app: Flask):
    app.add_url_rule('/', 'root', root)
    app.register_blueprint(api)
    app.register_blueprint(api_smp, url_prefix='/api/smp')


def setup_queue(app: Flask):
    app.queue = Queue(app.config)
    atexit.register(app.queue.shutdown)


def setup_logging(app: Flask):
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    default_level = 'debug' if app.config['DEBUG'] else 'info'
    address = app.config.get('LOG_ADDRESS', '/dev/log')
    facility = app.config.get('LOG_FACILITY', 'LOG_SYSLOG')
    level = app.config.get('LOG_LEVEL', default_level)
    handler = SysLogHandler(
        address=address,
        facility=SysLogHandler.__dict__[facility],
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

def create_app() -> Flask:
    """
    Using the app-factory pattern
    :return Flask:
    """
    app = Flask(
        __name__,
        static_folder='static',
        template_folder='templates'
    )
    app.config.from_object(APP_ENV)
    setup_routes(app)
    setup_queue(app)
    setup_logging(app)
    return app
