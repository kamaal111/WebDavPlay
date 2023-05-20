from rest_framework import mixins, viewsets
from rest_framework.request import Request
from rest_framework.decorators import action
from django.contrib.auth.models import User

from webdav.accounts.controllers import UserController
from webdav.accounts.serializers import UserSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer

    def create(self, request: Request):
        return UserController.create(request.data)

    @action(detail=False, methods=["POST"], url_path="login")
    def login(self, request: Request):
        return UserController.login(request.data)
