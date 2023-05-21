from rest_framework import viewsets, mixins
from rest_framework.response import Response

from webdav.contacts.models import Contact
from webdav.contacts.serializers import ContactSerializer


class ContactsViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Contact.objects.all().order_by("id")
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        serializer.validated_data.setdefault("user", self.request.user)
        return super().perform_create(serializer)

    def options(self, request, *args, **kwargs):
        response = super().options(request, *args, **kwargs)
        return Response(
            data=response.data,
            status=200,
            headers={**response.headers, "Allows": "OPTIONS GET HEAD POST DELETE"},  # type: ignore
        )
