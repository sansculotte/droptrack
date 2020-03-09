# -*- coding: utf-8 -*-
import atexit
from logging import Formatter
from logging.handlers import SysLogHandler
import os
from werkzeug.utils import secure_filename
from flask import (
    Flask,
    current_app,
    flash,
    Response,
    request,
    render_template,
    redirect,
    send_from_directory,
    url_for,
)
from .lib import (
    push_to_queue,
    validate_url,
    validate_soundfile,
    download
)
from webapp.queue import Queue


try:
    APP_ENV = os.environ['APP_ENV']
except KeyError:
    APP_ENV = 'config.Config'


def root():
    return render_template('url.html')


def url():
    """
    Accept soundfile url
    """
    if request.method == 'POST':
        url = request.form.get('url')
        if validate_url(url):
            push_to_queue(url)
            flash('JUHUUU Erfolg!')
        else:
            flash('Sorry, this did not work. Please try again')
    return redirect('/')


def upload():
    """
    Accept soundfile upload
    """
    if request.method == 'POST':
        soundfile = request.files.get('soundfile')
        if validate_soundfile(soundfile):
            filename = secure_filename(soundfile.filename)
            location = os.path.join(
                current_app.config['UPLOAD_DIR'],
                filename
            )
            soundfile.save(location)
            url = url_for('download', filename=filename, _external=True)
            push_to_queue(url)
            flash('JUHUUU Erfolg!')
        else:
            flash('Sorry. Upload Failed.')

    return redirect('/')


def download(filename):
    return send_from_directory(
        current_app.config['UPLOAD_DIR'],
        filename,
        as_attachment=True
    )


def setup_routes(app):
    url.methods = ['GET', 'POST']
    upload.methods = ['POST']
    app.add_url_rule('/', 'root', root)
    app.add_url_rule('/url', 'url', url)
    app.add_url_rule('/soundfile', 'upload', upload)
    app.add_url_rule('/soundfile/<path:filename>', 'download', download)


def setup_queue(app):
    app.queue = Queue(app.config)


def setup_logging(app):
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


def create_app():
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
    atexit.register(app.queue.shutdown)
    return app
