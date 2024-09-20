from rest_framework import serializers
from .models import CatalogCollectionMetaView, CcrView, RemView, AreasView, ResourceType, Product

class CatalogCollectionMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogCollectionMetaView
        fields = '__all__'
        #exclude = ('the_geom',)
        geo_field = 'the_geom'

    thumbnail_image = serializers.SerializerMethodField()
    def get_thumbnail_image(self, obj):
        if str(obj.thumbnail_image) != "" and obj.thumbnail_image is not None:
            path = str(obj.thumbnail_image)
        else:
            path = None
        return path

    tile_index_url = serializers.SerializerMethodField()
    def get_tile_index_url(self, obj):
        if str(obj.tile_index_url) != "" and obj.tile_index_url is not None:
            path = str(obj.tile_index_url)
        else:
            path = None
        return path

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CcrView
        fields = '__all__'

    thumbnail_image = serializers.SerializerMethodField()
    def get_thumbnail_image(self, obj):
        if str(obj.thumbnail_image) != "" and obj.thumbnail_image is not None:
            path = str(obj.thumbnail_image)
        else:
            path = None
        return path

    images = serializers.SerializerMethodField()
    def get_images(self, obj):
        if str(obj.images) != "" and obj.images is not None:
            path = str(obj.images)
        else:
            path = None
        return path

    tile_index_url = serializers.SerializerMethodField()
    def get_tile_index_url(self, obj):
        if str(obj.tile_index_url) != "" and obj.tile_index_url is not None:
            path = str(obj.tile_index_url)
        else:
            path = None
        return path

    supplemental_report_url = serializers.SerializerMethodField()
    def get_supplemental_report_url(self, obj):
        if str(obj.supplemental_report_url) != "" and obj.supplemental_report_url is not None:
            path = str(obj.supplemental_report_url)
        else:
            path = None
        return path

    lidar_breaklines_url = serializers.SerializerMethodField()
    def get_lidar_breaklines_url(self, obj):
        if str(obj.lidar_breaklines_url) != "" and obj.lidar_breaklines_url is not None:
            path = str(obj.lidar_breaklines_url)
        else:
            path = None
        return path

    lidar_buildings_url = serializers.SerializerMethodField()
    def get_lidar_buildings_url(self, obj):
        if str(obj.lidar_buildings_url) != "" and obj.lidar_buildings_url is not None:
            path = str(obj.lidar_buildings_url)
        else:
            path = None
        return path

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemView
        fields = ('__all__')

    resource = serializers.SerializerMethodField()
    def get_resource(self, obj):
        if str(obj.resource) != "" and obj.resource is not None:
            path = str(obj.resource)
        else:
            path = None
        return path

class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = '__all__'

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreasView
        fields = '__all__'


class ProdcutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'