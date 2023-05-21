from rest_framework import serializers

from webdav.contacts.models import Contact
from webdav.serializer_fields import BinaryField


class ContactSerializer(serializers.ModelSerializer):
    content = BinaryField(required=True)

    class Meta:
        model = Contact
        fields = ("id", "content")
