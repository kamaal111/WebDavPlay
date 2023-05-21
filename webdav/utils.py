import functools
from uuid import UUID

from webdav.exceptions import InvalidPayload


def validate_uuid_pk(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if pk := kwargs.get("pk"):
            try:
                UUID(pk)
            except ValueError:
                raise InvalidPayload("Invalid ID provided.")
        return func(*args, **kwargs)

    return wrapper
