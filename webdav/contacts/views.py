from rest_framework import viewsets, mixins
from webdav.contacts.controllers import ContactsController

from webdav.contacts.models import Contact
from webdav.contacts.serializers import ContactSerializer


class ContactsViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION")
        return ContactsController.create(request.data, token)
