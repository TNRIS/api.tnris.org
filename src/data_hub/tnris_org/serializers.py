from rest_framework import serializers

from .models import (
    TnrisTraining,
    TnrisForumTraining,
    TnrisInstructorType,
    CompleteForumTrainingView,
    TnrisGioCalendarEvent,
    TnrisDocument
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


class TnrisGioCalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TnrisGioCalendarEvent
        # fields = '__all__'
        fields = ('title',
                  'location',
                  'start_date',
                  'end_date',
                  'start_time',
                  'end_time',
                  'short_description',
                  'event_url',
                  'community_meeting',
                  'community_meeting_agenda_url',
                  'solutions_group_meeting',
                  'public',
                  'street_address',
                  'city',
                  'state',
                  'zipcode',
                  'pretty_date',
                  'pretty_time')

    # pretty format date/time for api rest endpoint to use on front end
    pretty_date = serializers.SerializerMethodField()
    pretty_time = serializers.SerializerMethodField()

    def get_pretty_date(self, obj):
        sd = obj.start_date
        ed = obj.end_date
        pd = ''
        # if end_date is not populated or is same as start_date, just use start_date
        if ed is None or sd == ed:
            pd = sd.strftime('%B %-d, %Y')
        # otherwise, handle end_date
        else:
            # if different years, format range with month, day, & year
            if sd.year != ed.year:
                pd = sd.strftime('%B %-d, %Y') + "-" + ed.strftime('%B %-d, %Y')
            # otherwise, handle month difference
            else:
                # if different months, format range with month, day and shared year
                if sd.month != ed.month:
                    pd = sd.strftime('%B %-d') + "-" + ed.strftime('%B %-d, %Y')
                # otherwise, format range with day and shared month & year
                else:
                    pd = sd.strftime('%B %-d') + "-" + ed.strftime('%-d, %Y')
        return pd

    def get_pretty_time(self, obj):
        st = obj.start_time
        et = obj.end_time
        pt = None
        # if both start_time and end_time populated, make pretty
        if st is not None and et is not None:
            pt = "%s-%s" % (st.strftime('%I:%M%p').lstrip("0"),
                            et.strftime('%I:%M%p').lstrip("0"))
        return pt


class TnrisSGMDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TnrisDocument
        fields = ('document_id',
                  'document_name',
                  'document_url',
                  'sgm_note',
                  'created',
                  'last_modified',)
