from rest_framework.exceptions import APIException
from http.client import UNAUTHORIZED


class Unauthorized(APIException):
    status_code = UNAUTHORIZED
    default_detail = "Unauthorized."
    default_code = "unauthorized"