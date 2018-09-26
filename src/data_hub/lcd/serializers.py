from rest_framework import serializers

from .models import CcrView, RemView, AcdcView


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CcrView
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemView
        fields = ('__all__')

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcdcView
        fields = '__all__'


#
# -------------------------------------
#
# EVEYTHING BELOW THIS LINE CAN BE DELETED.
# Reminents from data concierge
#
# -------------------------------------
#
#

# class ProductSerializer(serializers.ModelSerializer):
#
#     """This serializer is the main class for creating the API
#     response at v1.
#
#     example: ... /api/v1/records?countyFips=48355
#     """
#
#     CountyFIPS = serializers.SerializerMethodField('county_fips')
#     AcquiringAgency = serializers.SlugField(
#         source="collection.agency.name", read_only=True)
#     Date = serializers.DateField(source="collection.from_date", read_only=True)
#     NumFrames = serializers.IntegerField(
#         source="number_of_frames", read_only=True)
#     PrintType = serializers.SlugField(source="print_type", read_only=True)
#     Scale = serializers.IntegerField(source="scale.scale", read_only=True)
#
#     def county_fips(self, product):
#         fips = self.context['request'].query_params.get('countyFips')
#         return fips
#
#     class Meta:
#         model = Product
#         fields = ('AcquiringAgency', 'CountyFIPS', 'Date', 'NumFrames',
#                   'PrintType', 'Scale')
