from rest_framework import viewsets, mixins
from rest_framework.request import Request

from webdav.contacts.controllers import ContactsController
from webdav.contacts.models import Contact
from webdav.contacts.serializers import ContactSerializer


class ContactsViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request: Request):
        return ContactsController.create(payload=request.data, user=request.user)
