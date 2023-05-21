from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import Http404, HttpRequest

from webdav.contacts.models import Contact, ContactManager
from webdav.contacts.serializers import ContactSerializer
from webdav.utils import validate_uuid_pk


class ContactsViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Contact.objects.all().order_by("id")
    serializer_class = ContactSerializer

    def filter_queryset(self, queryset: ContactManager):
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data.setdefault("user", self.request.user)
        if id := self.kwargs.get("pk"):
            serializer.validated_data.setdefault("id", id)

        return super().perform_create(serializer)

    @validate_uuid_pk
    def update(self, request: Request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Http404:
            return self.create(request, *args, **kwargs)
        except Exception:
            raise  # unknown exception

    def options(self, request: HttpRequest, *args, **kwargs):
        response = super().options(request, *args, **kwargs)
        return Response(
            data=response.data,
            status=200,
            headers={**response.headers, "Allows": "OPTIONS GET HEAD POST DELETE"},  # type: ignore
        )

    def create(self, request: Request, *args, **kwargs):
        if request.method != "PUT":
            raise Http404

        return super().create(request, *args, **kwargs)

    def partial_update(self, request: Request, *args, **kwargs):
        raise Http404
