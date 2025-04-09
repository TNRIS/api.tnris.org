from rest_framework import serializers

from .models import (
    Campaign,
    CampaignSubscriber,
    DataHubContact,
    DataHubOrder,
    DataHubOutsideEntityContact,
    EducationContact,
    ForumJobBoardSubmission,
    GeneralContact,
    GeorodeoCallForPresentationsSubmission,
    GeorodeoRegistration,
    LakesOfTexasContact,
    OrderMap,
    OrderType,
    PosterGallerySubmission,
    SurveyTemplate,
    TexasImageryServiceContact,
    TexasImageryServiceRequest
)


class DataHubContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataHubContact
        fields = ('__all__')

class DataHubOutsideEntityContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataHubOutsideEntityContact
        fields = ('__all__')


class EducationContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationContact
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


class OrderMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMap
        fields = ('__all__')
        
        
class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderType
        fields = ('__all__')
        

class PosterGallerySubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosterGallerySubmission
        fields = ('__all__')

class CampaignSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignSubscriber
        fields = ('__all__')

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('__all__')

class SurveyTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyTemplate
        fields = ('__all__')

class TexasImageryServiceContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = TexasImageryServiceContact
        fields = ('__all__')

class TexasImageryServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TexasImageryServiceRequest
        fields = ('__all__')