from typing import Optional, Union

import uuid
from sqlalchemy.types import TypeDecorator, BINARY, CHAR
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from webapp.lib.security import PasswordHash


class Password(TypeDecorator):
    """
    Automaticly hash and unhash passwords in and out of the database
    """
    impl = CHAR(166)

    def process_bind_param(
        self,
        value: Union[str, PasswordHash, None],
        _dialect
    ) -> str:
        """Ensure the value is a PasswordHash and then return its hash."""
        if value is None:
            return ''
        else:
            return self._convert(value).hash

    def process_result_value(
        self,
        value: Optional[str],
        dialect
    ) -> Optional[PasswordHash]:
        """Convert the hash to a PasswordHash, if it's non-NULL."""
        if value is None:
            return None
        else:
            return PasswordHash(value)

    def validator(self, password: str):
        """Provides a validator/converter for @validates usage."""
        return self._convert(password)

    def _convert(self, value: Union[str, PasswordHash]) -> PasswordHash:
        """Returns a PasswordHash from the given string.

        PasswordHash instances or None values will return unchanged.
        Strings will be hashed and the resulting PasswordHash returned.
        Any other input will result in a TypeError.
        """
        if isinstance(value, PasswordHash):
            return value
        elif isinstance(value, str):
            return PasswordHash.new(value)
        elif value is not None:
            raise TypeError(f'Cannot convert {type(value)} to a PasswordHash')
        else:
            raise TypeError('Empty Field can not be converted')


class UUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    BINARY(16), to store UUID.

    """
    impl = BINARY

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PostgresUUID())
        else:
            return dialect.type_descriptor(BINARY(16))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                if isinstance(value, bytes):
                    value = uuid.UUID(bytes=value)
                elif isinstance(value, int):
                    value = uuid.UUID(int=value)
                elif isinstance(value, str):
                    value = uuid.UUID(value)
        if dialect.name == 'postgresql':
            return str(value)
        else:
            return value.bytes

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if dialect.name == 'postgresql':
            return uuid.UUID(value)
        else:
            return uuid.UUID(bytes=value)
