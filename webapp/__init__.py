# -*- coding: utf-8 -*-
import string, random
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
# from .session import dtsession

############################################################
# data

try:
    APP_ENV = os.environ['APP_ENV']
except KeyError:
    APP_ENV = 'config.Config'

def generate_username(length=4):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    # print("    generate_username: random string of length", length, "is:", result_str)
    return result_str

def dt_session_dir_make(dt_session):
    dt_session_dir_path = os.path.join(
        current_app.config['DATA_DIR'],
        'dt_sessions',
        dt_session
    )

    for subdir in ['uploaded', 'generated']:
        dt_session_dir_path_subdir = os.path.join(
            dt_session_dir_path,
            subdir
        )
        # exist, done
        if os.path.exists(dt_session_dir_path_subdir):
            if f'dt_session_dir_path_{subdir}' not in session:
                session[f'dt_session_dir_path_{subdir}'] = dt_session_dir_path_subdir
            continue
        else:
            # make it
            try:
                os.makedirs(dt_session_dir_path_subdir)
                session[f'dt_session_dir_path_{subdir}'] = dt_session_dir_path_subdir
            except Exception as e:
                pass

    return True

def dt_session_check(session, request):
    dt_session_new = False
    if 'dt_session' in session:
        dt_session = session['dt_session']
    elif 'dt_session' not in session and 'dt_session' in request.cookies:
        session['dt_session'] = request.cookies['dt_session']
        dt_session = session['dt_session']
    else:
        dt_session = generate_username(length=4)
        session['dt_session'] = dt_session
        dt_session_new = True
        
    # create session directory
    dt_session_dir_make(dt_session)
        
    return dt_session_new
        
def root():
    # check session
    dt_session_new = dt_session_check(session, request)

    # create response
    resp = make_response(render_template('main.html'))

    # if new session set cookie
    if dt_session_new:
        resp.set_cookie('dt_session', session['dt_session'])

    # return response
    return resp

def setup_routes(app: Flask):
    app.add_url_rule('/', 'root', root)
    app.register_blueprint(api)


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


def setup_data(app: Flask):
    dt_data = {
        'zniz': {'path': os.path.join(app.config.get('DATA_DIR'), 'dt_sessions', 'zniz')},
        'zniz_ul': {'path': os.path.join(app.config.get('DATA_DIR'), 'dt_sessions', 'zniz', 'uploaded')},
        'zniz_gt': {'path': os.path.join(app.config.get('DATA_DIR'), 'dt_sessions', 'zniz', 'generated')},
        'zniz_ul_trk009-3.mp3': {'path': os.path.join(app.config.get('DATA_DIR'), 'dt_sessions', 'zniz', 'uploaded', 'trk009-3.mp3')},
        'zniz_ul_trk010-3.mp3': {'path': os.path.join(app.config.get('DATA_DIR'), 'dt_sessions', 'zniz', 'uploaded', 'trk010-3.mp3')},
        'zniz_ul_trk011-3.mp3': {'path': os.path.join(app.config.get('DATA_DIR'), 'dt_sessions', 'zniz', 'uploaded', 'trk011-3.mp3')},
    }
    app.dt_data = dt_data


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
    setup_data(app)
    return app
