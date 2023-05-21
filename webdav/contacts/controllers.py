from http.client import CREATED
from typing import Any
from rest_framework.response import Response
from django.contrib.auth.models import User

from webdav.contacts.serializers import ContactSerializer


class ContactsController:
    @classmethod
    def create(cls, payload: Any, user: User):
        contact = ContactSerializer(data=payload)
        contact.is_valid(raise_exception=True)

        created_contact = contact.create({**contact.data, "user": user})

        return Response({"id": created_contact.id}, status=CREATED)
