from http.client import CONFLICT
from rest_framework.exceptions import APIException


class UserAlreadyExists(APIException):
    status_code = CONFLICT
    default_detail = "User already exists."
    default_code = "user_conflict"
