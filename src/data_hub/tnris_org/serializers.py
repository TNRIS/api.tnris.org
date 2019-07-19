from rest_framework import serializers

from .models import (TnrisTraining, TnrisForumTraining)
from datetime import datetime


class TnrisTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TnrisTraining
        fields = '__all__'

    # format date/time for api rest endpoint to use on front end
    start_date_time = serializers.DateTimeField(format="%A, %B %d %I:%M %p")
    end_date_time = serializers.DateTimeField(format="%A, %B %d %I:%M %p")


class TnrisForumTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TnrisForumTraining
        fields = '__all__'

    # format date/time for api rest endpoint to use on front end
    start_date_time = serializers.DateTimeField(format="%A, %B %d %I:%M %p")
    end_date_time = serializers.DateTimeField(format="%A, %B %d %I:%M %p")
