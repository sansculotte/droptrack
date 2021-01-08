from typing import Optional, Union
from sqlalchemy.types import TypeDecorator, CHAR
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
