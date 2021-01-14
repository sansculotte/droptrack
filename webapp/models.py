from typing import Optional

import os
from uuid import uuid4
from enum import Enum
from flask import current_app, url_for
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from webapp.lib.security import generate_password
from .type_decorators import Password, UUID


db: SQLAlchemy = SQLAlchemy()


class Status(Enum):
    processing = 10
    done = 20
    error = 30


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=64), nullable=False, unique=True)
    email = db.Column(db.String(length=128), nullable=True, unique=True)
    password = db.Column(Password())
    api_key = db.Column(db.String(length=128), nullable=True, unique=True)
    tasks = db.relationship('Task', backref='user', cascade="all,delete")

    @staticmethod
    def find_by_api_key(token: str) -> Optional['User']:
        """
        Find User by API token
        """
        if token:
            return User.query.filter_by(api_key=token).first()
        return None

    @staticmethod
    def find_by_name(name: str) -> Optional['User']:
        """
        Find User by name
        """
        if name:
            return User.query.filter_by(name=name).first()
        return None

    @staticmethod
    def create(name: str, email: str, password: str) -> 'User':
        """
        create new User
        """
        password = password or generate_password()

        user = User(name=name, email=email, password=password)

        try:
            user.make_home_directory()
        except FileExistsError:
            current_app.logger.warn('home directory {user.name} already exists')

        return user

    def check_password(self, password: str):
        return self.password == password

    @property
    def home_directory(self):
        assert self.name
        return os.path.join(current_app.config['UPLOAD_DIR'], self.name)

    def make_home_directory(self):
        os.mkdir(self.home_directory)


class Task(db.Model):

    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(), unique=True, nullable=False, default=uuid4)
    name = db.Column(db.String(length=64), nullable=False)
    status = db.Column(db.Enum(Status), default=Status.processing)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    result_location = db.Column(db.String(256))  # path to resource/file

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uuid = self.uuid or uuid4()
        self.status = self.status or Status.processing

    @staticmethod
    def find_by_uuid(uuid: str) -> Optional['Task']:
        return Task.query.filter_by(uuid=uuid).first()

    @property
    def url(self) -> str:
        """
        Return url to result file if there is one,
        otherwise the task url
        """
        if self.result_location:
            return url_for(
                'api.download_file',
                filename=self.result_location,
                _external=True
            )
        else:
            return url_for('api.show_task', uuid=self.uuid, _external=True)

    @property
    def is_processing(self):
        return self.status == Status.processing

    @property
    def is_done(self):
        return self.status == Status.done

    def set_done(self, result_location: Optional[str] = None):
        """
        Resolve task, optionally set path to result file
        """
        self.result_location = result_location
        self.status = Status.done
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        """
        Export for JSON serializer
        """
        return {
            'name': self.name,
            'uuid': str(self.uuid),
            'url': self.url,
            'status': self.status.name
        }
