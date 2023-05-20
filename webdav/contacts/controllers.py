from http.client import CREATED
from typing import Any
from rest_framework.response import Response

from webdav.accounts.services import AuthenticationService
from webdav.contacts.serializers import ContactSerializer
from webdav.exceptions import Unauthorized


class ContactsController:
    authentication = AuthenticationService()

    @classmethod
    def create(cls, payload: Any, token: str | None):
        if not token:
            raise Unauthorized

        contact = ContactSerializer(data=payload)
        contact.is_valid(raise_exception=True)

        authenticated_token = cls.authentication.authenticated_token(token=token)
        user = authenticated_token.user

        created_contact = contact.create({**contact.data, "user": user})

        return Response({"id": created_contact.id}, status=CREATED)
