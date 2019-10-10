from rest_framework import serializers

from .models import (
    DataHubContact,
    DataHubOrder,
    ForumJobBoardSubmission,
    GeneralContact,
    GeorodeoCallForPresentationsSubmission,
    GeorodeoRegistration,
    LakesOfTexasContact,
    PosterGallerySubmission,
    TexasImageryServiceContact,
    TexasImageryServiceRequest
)


class DataHubContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataHubContact
        fields = ('__all__')


class DataHubOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataHubOrder
        fields = ('__all__')

        
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


class LakesOfTexasContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = LakesOfTexasContact
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
