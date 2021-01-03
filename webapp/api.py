"""droptrack.webapp.api

The main mechanics of the webapp.

This is NOT proper REST.
"""


from typing import Optional
import os
from flask import (
    g,
    current_app,
    json,
    jsonify,
    request,
    url_for,
    session,
    send_from_directory,
    Blueprint,
    Response,
)
from werkzeug.utils import secure_filename
from .lib import (
    validate_url,
    validate_soundfile,
)
from .models import User
"""
The main mechanics of the webapp.
"""

api = Blueprint('api', __name__)

@api.before_request
def authenticate() -> Optional[Response]:
    """
    verify token, bind user to request global
    """
    token = request.headers.get('X-Authentication')
    if token:
        g.user = User.verify_api_token(token)
        return None
    else:
        return not_authorized()


def not_authorized(error=None, message='not authorized') -> Response:
    return api_response_error({'message': message}, status=403)


def api_response_ok(data: dict, status: int = 200) -> Response:
    data.update({'status': 'ok'})
    return Response(json.dumps(data), status=status)


def api_response_started(data: dict) -> Response:
    data.update({'status': 202})
    return jsonify(data)


def api_response_error(data: dict, status: int = 400) -> Response:
    data.update({'status': 'error'})
    return Response(json.dumps(data), status=status)


@api.route('/url', methods=['POST'])
def url() -> Response:
    """
    Accept soundfile url
    """
    # TODO: requires server/player to be up to do the actual download
    if request.method == 'POST':
        url = request.json.get('url')
        if validate_url(url):
            current_app.queue.send(url)
            return api_response_ok({'message': 'Url accepted'})
        else:
            return api_response_error({'message': 'Invalid url'})
    return Response(status=405)


@api.route('/files', methods=['POST'])
def upload() -> Response:
    """
    Accept direct soundfile upload per multipart/form-data
    """
    if request.method == 'POST':
        soundfile = request.files.get('soundfile')
            
        if soundfile and validate_soundfile(soundfile):
            filename = secure_filename(soundfile.filename)

            # make sure home directory exists.
            if not os.path.exists(g.user.home_directory):
                g.user.make_home_directory()
                current_app.logger.info(
                    f'User Home directory created {g.user.home_directory}'
                )

            location = os.path.join(
                g.user.home_directory,
                filename
            )
            soundfile.save(location)
            
            # trigger player for redownload
            url = url_for('api.download', filename=filename, _external=True)
            current_app.queue.send(url)

            # return response
            return api_response_ok({
                'message': 'File accepted',
                'soundfilesize': soundfilesize,
            })
        else:
            return api_response_error({'message': 'Invalid File'})
    return Response(status=405)


@api.route('/files/<string:filename>', methods=['GET'])
def download(filename: str) -> Response:
    """
    Retrieve stored file
    """
    current_app.logger.info(f'api.download filename {filename}')
    current_app.logger.info(f'api.download g.user.home_directory {g.user.home_directory}')
    return api_response_ok({'message': 'api.download'})
    # return send_from_directory(
    #     g.user.home_directory,
    #     filename,
    #     as_attachment=True
    # )
    

@api.route('/files/<string:filename>', methods=['DELETE'])
def delete_file(filename: str) -> Response:
    """
    Delete stored file
    """
    location = os.path.join(
        g.user.home_directory,
        filename
    )
    os.unlink(location)
    return api_response_ok({'message': 'file deleted'})
