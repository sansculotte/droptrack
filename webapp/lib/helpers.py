from typing import Optional
from flask import current_app
from werkzeug.datastructures import FileStorage
from urllib.parse import urlparse


def file_allowed(filename: str) -> bool:
    allowed_extensions = current_app.config['UPLOAD_ALLOWED_EXTENSIONS']
    return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions


def validate_url(url: str) -> bool:
    return url.startswith('http://') \
        or url.startswith('https://')


def validate_soundfile(soundfile: Optional[FileStorage]) -> bool:
    if soundfile and soundfile.filename:
        return file_allowed(soundfile.filename)
    else:
        return False
