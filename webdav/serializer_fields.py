from rest_framework import serializers


class BinaryField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        if isinstance(data, bytes):
            return data

        self.fail("invalid")
