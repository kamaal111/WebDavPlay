from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.http import Http404
from rest_framework.authtoken.models import Token

from webdav.exceptions import Unauthorized


class AuthenticationService:
    def __init__(self) -> None:
        ...

    def authenticated_token(self, token: str):
        if "Bearer" in token:
            splitted_token = token.split(" ")
            if len(splitted_token) != 2:
                raise Unauthorized
            token = splitted_token[1]

        try:
            return Token.objects.get(key=token)
        except Token.DoesNotExist as e:
            raise Unauthorized from e

    def get_user_token(self, username: str | None, email: str | None, password: str):
        user = self.__get_authorized_user(
            username=username, email=email, password=password
        )
        token, _ = Token.objects.get_or_create(user=user)
        return token

    def __get_authorized_user(
        self, username: str | None, email: str | None, password: str
    ):
        try:
            if username:
                user = User.objects.get(username=username)
            else:
                assert email is not None, "Email should have existed at this point"
                user = User.objects.get(email=email)
        except User.DoesNotExist as e:
            raise Http404 from e

        if not check_password(password, user.password):
            raise Unauthorized

        return user
