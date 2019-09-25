from rest_framework import serializers

from .models import (
    GeneralContact
)


class GeneralContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralContact
        fields = ('__all__')
