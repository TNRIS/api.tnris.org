from rest_framework import serializers

from .models import (TnrisTraining, TnrisForumTraining)

class TnrisTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TnrisTraining
        fields = '__all__'


class TnrisForumTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TnrisForumTraining
        fields = '__all__'
