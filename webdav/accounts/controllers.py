from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from rest_framework.response import Response
from http.client import CREATED, OK


from webdav.accounts.exceptions import UserAlreadyExists
from webdav.accounts.serializers import CredentialsSerializer, UserSerializer
from webdav.services import AuthenticationService


class UserController:
    authentication = AuthenticationService()

    @staticmethod
    def create(payload: Any):
        user = UserSerializer(data=payload)
        user.is_valid(raise_exception=True)
        validated_user = user.validated_object

        try:
            User.objects.get(
                Q(username=validated_user.username) | Q(email=validated_user.email)
            )
        except User.DoesNotExist:
            pass
        else:
            raise UserAlreadyExists

        user.create({**user.data, "password": make_password(validated_user.password)})

        response = user.data
        response.pop("password")
        return Response(response, status=CREATED)

    @classmethod
    def login(cls, payload: Any):
        credentials = CredentialsSerializer(data=payload)
        credentials.is_valid(raise_exception=False)
        validated_credentials = credentials.validated_object

        token = cls.authentication.get_user_token(
            username=validated_credentials.username,
            email=validated_credentials.email,
            password=validated_credentials.password,
        )

        return Response({"token": token.key}, status=OK)
