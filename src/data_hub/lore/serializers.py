from rest_framework import serializers

from .models import (County, CountyRelate, Product, ChcView)


class CountySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = County
        fields = ('fips', 'name')


class ProductSerializer(serializers.ModelSerializer):

    """This serializer is the main class for creating the API
    response at v1.

    example: ... /api/v1/records?countyFips=48355
    """

    CountyFIPS = serializers.SerializerMethodField('county_fips')
    AcquiringAgency = serializers.SlugField(
        source="collection.agency.name", read_only=True)
    Date = serializers.DateField(source="collection.from_date", read_only=True)
    NumFrames = serializers.IntegerField(
        source="number_of_frames", read_only=True)
    PrintType = serializers.SlugField(source="print_type", read_only=True)

    def county_fips(self, product):
        fips = self.context['request'].query_params.get('countyFips')
        return fips

    class Meta:
        model = Product
        fields = ('AcquiringAgency', 'CountyFIPS', 'Date', 'NumFrames',
                  'PrintType')


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChcView
        fields = '__all__'

    s_three_key = serializers.SerializerMethodField()
    def get_s_three_key(self, obj):
        try:
            if(obj.source_abbreviation and obj.from_date and obj.collection):
                sa = obj.source_abbreviation
                year = obj.from_date.strftime("%Y")
                cname = obj.collection
                return sa + '-' + year + '-' + cname
            else:
                return ""
        except:
            return ""

    thumbnail_image = serializers.SerializerMethodField()
    def get_thumbnail_image(self, obj):
        if str(obj.thumbnail_image) != "" and obj.thumbnail_image is not None:
            path = str(obj.thumbnail_image).replace("https://s3.amazonaws.com/data.tnris.org/", "https://data.tnris.org/")
        else:
            path = None
        return path

    images = serializers.SerializerMethodField()
    def get_images(self, obj):
        if str(obj.images) != "" and obj.images is not None:
            path = str(obj.images).replace("https://s3.amazonaws.com/data.tnris.org/", "https://data.tnris.org/")
        else:
            path = None
        return path

    scanned_index_ls4_links = serializers.SerializerMethodField()
    def get_scanned_index_ls4_links(self, obj):
        if str(obj.scanned_index_ls4_links) != "" and obj.scanned_index_ls4_links is not None:
            path = str(obj.scanned_index_ls4_links).replace("https://s3.amazonaws.com/tnris-ls4/", "https://cdn.tnris.org/")
        else:
            path = None
        return path
