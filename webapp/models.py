import os
from typing import Optional
from flask import current_app
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from .type_decorators import Password
from webapp.lib.security import generate_password


db: SQLAlchemy = SQLAlchemy()


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=64), nullable=False, unique=True)
    email = db.Column(db.String(length=128), nullable=True, unique=True)
    password = db.Column(Password())
    api_key = db.Column(db.String(length=128), nullable=True, unique=True)

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
