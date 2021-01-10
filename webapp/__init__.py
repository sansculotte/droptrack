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

############################################################
# data

try:
    APP_ENV = os.environ['APP_ENV']
except KeyError:
    APP_ENV = 'config.Config'

print(APP_ENV)
    

if 'APP_ENV_BACKEND_USER' in os.environ and os.environ['APP_ENV_BACKEND_USER'] == 'postgres':
    from .models_postgres import db
    from flask_migrate import Migrate  # type: ignore
elif 'APP_ENV_BACKEND_USER' in os.environ and os.environ['APP_ENV_BACKEND_USER'] == 'plain':
    from .models_plain import db
    from .models_plain import Migrate

    
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
    address = app.config.get('LOG_ADDRESS', '/dev/log')
    facility = app.config.get('LOG_FACILITY', 'LOG_SYSLOG')
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
    db.init_app(app)
    setup_routes(app)
    setup_queue(app)
    setup_logging(app)
    if app.config['BACKEND_USER']:
        Migrate(app, db)

    @app.shell_context_processor
    def shell_context():
        return {'app': app, 'db': db}

    return app
