from http.client import CONFLICT, BAD_REQUEST
from rest_framework.exceptions import APIException


class InvalidPayload(APIException):
    status_code = BAD_REQUEST
    default_code = "bad_request"

    def __init__(self, detail: str, code=None):
        super().__init__(detail, code)


class UserAlreadyExists(APIException):
    status_code = CONFLICT
    default_detail = "User already exists."
    default_code = "user_conflict"
