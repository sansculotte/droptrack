# -*- coding: utf-8 -*-
import atexit
import os
from werkzeug.utils import secure_filename
from flask import (
    Flask,
    Response,
    request,
    render_template,
)
from .lib import (
    push_to_queue,
    validate_url,
    validate_soundfile,
    download
)
from .queue import Queue


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
    result = None
    if request.method == 'POST':
        url = request.form.get('url')
        if validate_url(url):
            push_to_queue(url)
            result = {'message': 'JUHUUU Erfolg!'}
        else:
            result = {'message': 'Sorry. Please try again'}

    return render_template('url.html', result=result)


def upload():
    """
    Accept soundfile upload
    """
    result = None
    if request.method == 'POST':
        soundfile = request.files.get('soundfile')
        if validate_soundfile(soundfile):
            filename = secure_filename(soundfile.filename)
            location = os.path.join(current_app.config['UPLOAD_DIR'], filename)
            soundfile.save(location)
            url = 'file://{}'.format(location)
            push_to_queue(url)
            result = {'message': 'JUHUUU Erfolg!'}
        else:
            result = {'message': 'Sorry. Upload failed'}

    return render_template('url.html', result=result)


def setup_routes(app):
    url.methods = ['GET', 'POST']
    upload.methods = ['POST']
    app.add_url_rule('/', 'root', root)
    app.add_url_rule('/url', 'url', url)
    app.add_url_rule('/soundfile', 'soudfile', upload)


def setup_queue(app):
    app.queue = Queue(app.config)


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
    atexit.register(app.queue.shutdown)
    return app
