from rest_framework import serializers

from .models import (
    GeneralContact,
    PosterGallerySubmission,
    TexasImageryServiceContact,
    TexasImageryServiceRequest
)


class GeneralContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralContact
        fields = ('__all__')


class PosterGallerySubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosterGallerySubmission
        fields = ('__all__')


class TexasImageryServiceContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = TexasImageryServiceContact
        fields = ('__all__')


class TexasImageryServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TexasImageryServiceRequest
        fields = ('__all__')
