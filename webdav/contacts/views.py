from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import FileUploadParser
from django.http import Http404, HttpRequest

from webdav.contacts.models import Contact, ContactManager
from webdav.contacts.serializers import ContactSerializer
from webdav.exceptions import InvalidPayload
from webdav.utils import validate_uuid_pk


class ContactsViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Contact.objects.all().order_by("id")
    serializer_class = ContactSerializer
    parser_classes = [FileUploadParser]

    def filter_queryset(self, queryset: ContactManager):
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data.setdefault("user", self.request.user)
        if id := self.kwargs.get("pk"):
            serializer.validated_data.setdefault("id", id)

        return super().perform_create(serializer)

    @validate_uuid_pk
    def update(self, request, *args, **kwargs):
        file = request.data.get("file")
        if file is None:
            raise InvalidPayload("No file provided.")

        request.data.setdefault("content", file.read())

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

        if id := kwargs.get("pk"):
            try:
                Contact.objects.get(id=id)
            except Contact.DoesNotExist:
                pass
            else:
                raise InvalidPayload("Invalid ID provided.")

        return super().create(request, *args, **kwargs)

    def partial_update(self, request: Request, *args, **kwargs):
        raise Http404
