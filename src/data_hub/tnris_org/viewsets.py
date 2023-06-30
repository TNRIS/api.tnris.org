from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from datetime import datetime
from modules import api_helper
import logging, watchtower

logger = logging.getLogger("errLog")
logger.addHandler(watchtower.CloudWatchLogHandler())

import boto3
from .models import (
    TnrisTraining,
    TnrisForumTraining,
    TnrisInstructorType,
    CompleteForumTrainingView,
    TnrisGioCalendarEvent,
    TnrisDocument,
    TrainingCategory,
    TnrisImage
)
from .serializers import (
    TnrisTrainingSerializer,
    TnrisForumTrainingSerializer,
    TnrisInstructorTypeSerializer,
    CompleteForumTrainingViewSerializer,
    TnrisGioCalendarEventSerializer,
    TnrisSGMDocumentSerializer,
    TnrisCommunityMeetingDocumentSerializer,
    TnrisCarouselImageSerializer
)


# actual db table; regular training api endpoint
class TnrisTrainingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve current TNRIS training schedule
    """
    serializer_class = TnrisTrainingSerializer
    http_method_names = ['get']

    def get_queryset(self):
        args = {'public': True}
        null_list = ['null', 'Null', 'none', 'None']
        # create argument object of query clauses
        for field in self.request.query_params.keys():
            if field != 'limit' and field != 'offset':
                value = self.request.query_params.get(field)
                # convert null queries
                if value in null_list:
                    value = None
                if field == 'category':
                    value = TrainingCategory.objects.get(training_category=value).training_category_id
                args[field] = value
        # get records using query
        queryset = TnrisTraining.objects.filter(**args).order_by('title', 'start_date_time', 'end_date_time')
        return queryset


# actual db table; regular forum training api endpoint without instructor info
class TnrisForumTrainingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve TNRIS Texas GIS Forum event training records
    """
    serializer_class = TnrisForumTrainingSerializer
    http_method_names = ['get']

    def get_queryset(self):
        args = {'public': True}
        null_list = ['null', 'Null', 'none', 'None']
        # create argument object of query clauses
        for field in self.request.query_params.keys():
            if field != 'limit' and field != 'offset':
                value = self.request.query_params.get(field)
                # convert null queries
                if value in null_list:
                    value = None
                args[field] = value
        # get records using query
        queryset = TnrisForumTraining.objects.filter(**args).order_by('title', 'start_date_time', 'end_date_time')
        return queryset


# actual db table; api endpoint for instructor domain
class TnrisInstructorTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve TNRIS training instructor details
    """
    serializer_class = TnrisInstructorTypeSerializer
    http_method_names = ['get']

    def get_queryset(self):
        # get records using query
        queryset = TnrisInstructorType.objects.all()
        return queryset


# db view, not actual table; api endpoint for complete training records with instructor info
class CompleteForumTrainingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve all TNRIS training records with instructor information
    """
    serializer_class = CompleteForumTrainingViewSerializer
    http_method_names = ['get']

    def get_queryset(self):
        args = {'public': True}
        null_list = ['null', 'Null', 'none', 'None']
        # create argument object of query clauses
        for field in self.request.query_params.keys():
            if field != 'limit' and field != 'offset':
                value = self.request.query_params.get(field)
                # convert null queries
                if value in null_list:
                    value = None
                args[field] = value
        # get records using query
        queryset = CompleteForumTrainingView.objects.filter(**args).order_by('title', 'start_date_time', 'end_date_time')
        return queryset


# actual db table; gio calendar events api endpoint
class TnrisGioCalendarEventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve all future TNRIS GIO calendar events
    """
    serializer_class = TnrisGioCalendarEventSerializer
    http_method_names = ['get']

    def get_queryset(self):
        # return only public records for today or in the future
        # and ignore all events with a start_date older than today
        args = {
            'public': True,
            'start_date__gte': datetime.today()
        }
        null_list = ['null', 'Null', 'none', 'None']
        # create argument object of query clauses
        for field in self.request.query_params.keys():
            if field != 'limit' and field != 'offset':
                value = self.request.query_params.get(field)
                # convert null queries
                if value in null_list:
                    value = None
                args[field] = value
        # get records using query. order by chronological start
        queryset = TnrisGioCalendarEvent.objects.filter(**args).order_by('start_date', 'start_time')
        return queryset


class TnrisSGMDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve all Solutions Group Meeting Documents for tnris.org frontend
    """
    serializer_class = TnrisSGMDocumentSerializer
    http_method_names = ['get']

    def get_queryset(self):
        # get records using query
        args = {'sgm_note': True}
        # order by document file name
        queryset = TnrisDocument.objects.filter(**args).order_by('document_name')
        return queryset


class TnrisCommunityMeetingDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve all GIS Community Meeting Documents for tnris.org frontend
    """
    serializer_class = TnrisCommunityMeetingDocumentSerializer
    http_method_names = ['get']

    def get_queryset(self):
        # get records using query
        args = {'comm_note': True}
        # order by document file name
        queryset = TnrisDocument.objects.filter(**args).order_by('document_name')
        return queryset


class TnrisCarouselImageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve all Carousel Images in order for tnris.org frontend
    """
    serializer_class = TnrisCarouselImageSerializer
    http_method_names = ['get']

    # def get_ordering(self)

    def get_queryset(self):
        # get records using query
        args = {'carousel': True}
        # order by carousel_order then image_name
        queryset = TnrisImage.objects.filter(**args).order_by('carousel_order', 'image_name')
        return queryset


class TnrisMetricsViewSet(viewsets.ViewSet):
    """
    Retrieve download statistics for the current month
    """
    permission_classes = (AllowAny,)
    
    def create(self, request, format=None):
        try:
            s3_resource = boto3.resource('s3')
            s3_client = boto3.client('s3')
            analytics = s3_resource.Bucket("tnris-analytics")
            downloads = analytics.objects.filter(Prefix="analytics.html")

            resp = list(downloads)[0].get()['Body'].read()
            
            return Response(
                {"status": "success", "message": resp},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            if(api_helper.checkLogger()): 
                logger.error("Cannot retrieve download stats. Error: " + str(e))
