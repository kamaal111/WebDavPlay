from http.client import CONFLICT, UNAUTHORIZED, BAD_REQUEST
from rest_framework.exceptions import APIException


class InvalidPayload(APIException):
    status_code = BAD_REQUEST
    default_code = "bad_request"

    def __init__(self, detail: str, code=None):
        super().__init__(detail, code)


class Unauthorized(APIException):
    status_code = UNAUTHORIZED
    default_detail = "Unauthorized."
    default_code = "unauthorized"


class UserAlreadyExists(APIException):
    status_code = CONFLICT
    default_detail = "User already exists."
    default_code = "user_conflict"
