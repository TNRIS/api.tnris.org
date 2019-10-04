from rest_framework import serializers

from .models import (
    GeneralContact,
    TexasImageryServiceContact,
    TexasImageryServiceRequest
)


class GeneralContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralContact
        fields = ('__all__')


class TexasImageryServiceContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = TexasImageryServiceContact
        fields = ('__all__')


class TexasImageryServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TexasImageryServiceRequest
        fields = ('__all__')
