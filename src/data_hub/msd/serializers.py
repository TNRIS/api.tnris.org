from rest_framework import serializers

from .models import (MsdView)

class MapCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MsdView
        fields = '__all__'

    thumbnail_link = serializers.SerializerMethodField()
    def get_thumbnail_link(self, obj):
        if str(obj.thumbnail_link) != "" and obj.thumbnail_link is not None:
            path = str(obj.thumbnail_link).replace("https://s3.amazonaws.com/data.tnris.org/", "https://data.tnris.org/")
        else:
            path = None
        return path

    map_downloads = serializers.SerializerMethodField()
    def get_map_downloads(self, obj):
        if str(obj.map_downloads) != "" and obj.map_downloads is not None:
            path = str(obj.map_downloads).replace("https://s3.amazonaws.com/data.tnris.org/", "https://data.tnris.org/")
        else:
            path = None
        return path
