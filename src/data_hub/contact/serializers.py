from rest_framework import serializers

from .models import (
    ForumJobBoardSubmission,
    GeneralContact,
    GeorodeoCallForPresentationsSubmission,
    GeorodeoRegistration,
    PosterGallerySubmission,
    TexasImageryServiceContact,
    TexasImageryServiceRequest
)


class ForumJobBoardSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumJobBoardSubmission
        fields = ('__all__')
        

class GeneralContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralContact
        fields = ('__all__')


class GeorodeoCallForPresentationsSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeorodeoCallForPresentationsSubmission
        fields = ('__all__')


class GeorodeoRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeorodeoRegistration
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
