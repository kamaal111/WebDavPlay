from rest_framework import serializers

from webdav.contacts.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=True, min_length=30)

    class Meta:
        model = Contact
        fields = ("id", "content")
