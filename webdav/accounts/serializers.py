from dataclasses import dataclass
from rest_framework import serializers
from django.contrib.auth.models import User

from webdav.accounts.exceptions import InvalidPayload


@dataclass
class ValidatedUser:
    username: str
    email: str
    password: str


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(min_length=5, required=True)
    password = serializers.CharField(min_length=4, max_length=128, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    @property
    def validated_object(self):
        return ValidatedUser(**self.data)


@dataclass
class ValidateCredentials:
    username: str | None
    email: str | None
    password: str


class CredentialsSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=False, default=None)
    email = serializers.EmailField(min_length=5, required=False, default=None)
    password = serializers.CharField(min_length=4, max_length=128, required=True)

    class Meta:
        fields = ["username", "email", "password"]

    def validate(self, attrs):
        default_validation = super().validate(attrs)

        if not attrs["username"] and not attrs["email"]:
            raise InvalidPayload(detail="'username' or 'email' is required.")

        return default_validation

    @property
    def validated_object(self):
        return ValidateCredentials(**self.data)
