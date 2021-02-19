import atexit
from logging import Formatter
from logging.handlers import SysLogHandler
import json
import os
from werkzeug.exceptions import HTTPException
from flask import (
    Flask,
    render_template,
)
from flask_migrate import Migrate  # type: ignore
from .queue import Queue
from .api import api
from .models import db


try:
    APP_ENV = os.environ['APP_ENV']
except KeyError:
    APP_ENV = 'config.Config'


def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        'status': 'error',
        'data': {
            'name': e.name,
            'message': e.description
        }
    })
    response.content_type = "application/json"
    return response


def root():
    return render_template('main.html')


def setup_routes(app: Flask):
    app.add_url_rule('/', 'root', root)
    app.register_blueprint(api)

    try:
        from .api_smp import api_smp
    except Exception:
        app.logger.error('Could not import api_smp')
    else:
        app.register_blueprint(api_smp, url_prefix='/api')


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


def setup(app: Flask):
    setup_routes(app)
    setup_queue(app)
    setup_logging(app)
    app.register_error_handler(HTTPException, handle_exception)

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
    setup(app)
    Migrate(app, db)

    @app.shell_context_processor
    def shell_context():
        return {'app': app, 'db': db}

    return app
