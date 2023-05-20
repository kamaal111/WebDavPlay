from rest_framework import viewsets

from webdav.contacts.models import Contact
from webdav.contacts.serializers import ContactSerializer


class ContactsViewSet(viewsets.GenericViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
