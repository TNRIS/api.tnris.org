from rest_framework import serializers

from .models import (TnrisTraining, TnrisForumTraining)
from datetime import datetime


class TnrisTrainingSerializer(serializers.ModelSerializer):
    # add serializer method field 'year' to api
    year = serializers.SerializerMethodField('get_training_year')

    def get_training_year(self, obj):
        return obj.start_date_time.strftime("%Y")

    class Meta:
        model = TnrisTraining
        fields = '__all__'

    # format date/time for api rest endpoint to use on front end
    start_date_time = serializers.DateTimeField(format="%A, %B %d %I:%M %p")
    end_date_time = serializers.DateTimeField(format="%A, %B %d %I:%M %p")


class TnrisForumTrainingSerializer(serializers.ModelSerializer):
    # add serializer method field 'year' to api
    year = serializers.SerializerMethodField('get_training_year')

    def get_training_year(self, obj):
        return obj.start_date_time.strftime("%Y")

    class Meta:
        model = TnrisForumTraining
        fields = '__all__'

    # format date/time for api rest endpoint to use on front end
    start_date_time = serializers.DateTimeField(format="%A, %B %d %I:%M %p")
    end_date_time = serializers.DateTimeField(format="%A, %B %d %I:%M %p")
