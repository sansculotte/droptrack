from typing import Optional
import os
from werkzeug.security import check_password_hash, generate_password_hash


METHOD = 'pbkdf2:sha512'
SALT_LENGTH = 16


class PasswordHash():

    def __init__(self, h: str):
        assert len(h) == 165, 'pbkdf2:512 with 16 bytes salt is 165 chars.'
        assert h.count('$'), 'pbkdf2 hash should have 2x "$".'
        self.hash = h

    def __eq__(self, password: object) -> bool:
        """Hashes the candidate string and compares it to the stored hash."""
        if isinstance(password, str):
            password = password.encode('utf8')
            return check_password_hash(self.hash, password)
        return False

    def __repr__(self):
        """Simple object representation."""
        return '<%s>' % type(self).__name__

    @classmethod
    def new(cls, password: str) -> 'PasswordHash':
        """Creates a PasswordHash from the given password."""
        if isinstance(password, str):
            return cls(
                generate_password_hash(
                    password,
                    method=METHOD,
                    salt_length=SALT_LENGTH
                )
            )
        else:
            raise TypeError('Password must be unicode')


def generate_password(length: int = 16) -> str:
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890/*#+-_%&[()]=?"
    scope = len(chars)
    return ''.join(
        chars[c % scope] for c in os.urandom(length)
    )
