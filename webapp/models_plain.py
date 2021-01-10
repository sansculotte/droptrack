import os
from typing import Optional, Union
from flask import current_app
from dataclasses import dataclass


_users = [
    {
        'id': 1,
        'name': 'x',
        'api_token': 'yuOJX-8paOqRJR8iefr7vL-Ozu5owbSUtr8SIM0K1L1EKPB9mWjPM52nydMEFyl7',
    }
]


class db(object):
    @staticmethod
    def init_app(app):
        print(f"models_plain.db init_app {app}")
        pass

class Migrate(object):
    def __init__(self, app, db):
        pass
    

class Token:

    __token: str

    def __init__(self, token):
        assert len(token) == 64
        self.__token = token

    def __str__(self):
        return self.__token

    def __eq__(self, other: object):
        return str(self) == other


@dataclass
class User:

    id: int
    name: str
    api_token: str

    @staticmethod
    def find_by_api_key(token: str) -> Optional['User']:
        return User.verify_api_token(token)
    
    @staticmethod
    def verify_api_token(token: str) -> Optional['User']:
        if token:
            for user in _users:
                if user['api_token'] == token:
                    return User(**user)
        return None

    @property
    def home_directory(self):
        assert self.name
        return os.path.join(current_app.config['UPLOAD_DIR'], self.name)

    def make_home_directory(self):
        os.mkdir(self.home_directory)
        
# _users = [
#     {
#         'id': 1,
#         'name': 'x',
#         'api_token': 'yuOJX-8paOqRJR8iefr7vL-Ozu5owbSUtr8SIM0K1L1EKPB9mWjPM52nydMEFyl7',
#     }
# ]


# class UserPlain(object):
#     id = _users['id']
#     name = _users['name']
#     api_key = _users['api_token']
    
#     def __init__(self): pass
    
#     @staticmethod
#     def verify_api_token(token: str) -> Optional['User']:
#         if token:
#             for user in _users:
#                 if user['api_token'] == token:
#                     return User(**user)
#         return None



