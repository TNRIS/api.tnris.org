from rest_framework import serializers

from .models import (MsdView)

class MapCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MsdView
        fields = '__all__'
