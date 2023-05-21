from rest_framework import viewsets, mixins

from webdav.contacts.models import Contact
from webdav.contacts.serializers import ContactSerializer


class ContactsViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Contact.objects.all().order_by("id")
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        serializer.validated_data.setdefault("user", self.request.user)
        return super().perform_create(serializer)
