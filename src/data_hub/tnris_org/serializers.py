from rest_framework import serializers

from .models import (
    TnrisTraining,
    TnrisForumTraining,
    TnrisInstructorType,
    CompleteForumTrainingView
)
from datetime import datetime


class TnrisTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TnrisTraining
        fields = ('training_id',
                  'year', # models.py property method (field does not exist in db)
                  'start_date_time',
                  'end_date_time',
                  'title',
                  'instructor',
                  'cost',
                  'registration_open',
                  'description',
                  'created',
                  'last_modified',
                  'public',)

    # format date/time for api rest endpoint to use on front end
    start_date_time = serializers.DateTimeField(format="%A, %B %d %I:%M %p")
    end_date_time = serializers.DateTimeField(format="%A, %B %d %I:%M %p")


class TnrisInstructorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TnrisInstructorType
        fields = ('instructor_type_id',
                  'name',
                  'company',
                  'bio',
                  'headshot',)


class TnrisForumTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TnrisForumTraining
        fields = ('training_id',
                  'year', # models.py property method (field does not exist in db)
                  'start_date_time',
                  'end_date_time',
                  'training_day',
                  'title',
                  'cost',
                  'registration_open',
                  'location',
                  'room',
                  'max_students',
                  'description',
                  'teaser',
                  'created',
                  'last_modified',
                  'public',)

    # format date/time for api rest endpoint to use on front end
    start_date_time = serializers.DateTimeField(format="%A, %B %d %I:%M %p")
    end_date_time = serializers.DateTimeField(format="%A, %B %d %I:%M %p")


class CompleteForumTrainingViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompleteForumTrainingView
        fields = ('training_id',
                  'year', # models.py property method (field does not exist in db)
                  'start_date_time',
                  'end_date_time',
                  'training_day',
                  'title',
                  'cost',
                  'registration_open',
                  'location',
                  'room',
                  'max_students',
                  'description',
                  'teaser',
                  'instructor_info',
                  'public',)

    # format date/time for api rest endpoint to use on front end
    start_date_time = serializers.DateTimeField(format="%A, %B %d %I:%M %p")
    end_date_time = serializers.DateTimeField(format="%A, %B %d %I:%M %p")
