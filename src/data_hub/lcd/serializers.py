from rest_framework import serializers
from .models import CcrView, RemView, AreasView


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
        model = AreasView
        fields = '__all__'
