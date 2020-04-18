import os
from flask import (
    current_app,
    jsonify,
    request,
    url_for,
    send_from_directory,
    Blueprint,
    Response,
)
from werkzeug.utils import secure_filename
from .lib import (
    validate_url,
    validate_soundfile,
)
"""
The main mechanics of the webapp.
This is NOT proper REST.
"""

api = Blueprint('api', __name__)


def api_response_ok(data: dict) -> Response:
    data.update({'status': 'ok'})
    return jsonify(data)


def api_response_error(data: dict) -> Response:
    data.update({'status': 'error'})
    return jsonify(data)


@api.route('/url', methods=['POST'])
def url() -> Response:
    """
    Accept soundfile url
    """
    if request.method == 'POST':
        url = request.json.get('url')
        if validate_url(url):
            current_app.queue.send(url)
            return api_response_ok({'message': 'Url accepted'})
        else:
            return api_response_error({'message': 'Invalid url'})
    return Response(status=405)


@api.route('/upload', methods=['POST'])
def upload() -> Response:
    """
    Accept direct soundfile upload per multipart/form-data
    """
    if request.method == 'POST':
        soundfile = request.files.get('soundfile')
        if soundfile and validate_soundfile(soundfile):
            filename = secure_filename(soundfile.filename)
            location = os.path.join(
                current_app.config['UPLOAD_DIR'],
                filename
            )
            soundfile.save(location)
            url = url_for('api.download', filename=filename, _external=True)
            current_app.queue.send(url)
            return api_response_ok({'message': 'File accepted'})
        else:
            return api_response_error({'message': 'Invalid File'})
    return Response(status=405)

@api.route('/download/<string:filename>')
def download(filename: str) -> Response:
    return send_from_directory(
        current_app.config['UPLOAD_DIR'],
        filename,
        as_attachment=True
    )
