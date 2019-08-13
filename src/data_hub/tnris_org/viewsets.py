from rest_framework import viewsets
from rest_framework.response import Response

from .models import (
    TnrisTraining,
    TnrisForumTraining,
    TnrisInstructorType,
    CompleteForumTrainingView
)
from .serializers import (
    TnrisTrainingSerializer,
    TnrisForumTrainingSerializer,
    TnrisInstructorTypeSerializer,
    CompleteForumTrainingViewSerializer
)


# actual db table; regular training api endpoint
class TnrisTrainingViewSet(viewsets.ReadOnlyModelViewSet):
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
                args[field] = value
        # get records using query
        queryset = TnrisTraining.objects.filter(**args).order_by('title', 'start_date_time', 'end_date_time')
        return queryset


# actual db table; regular forum training api endpoint without instructor info
class TnrisForumTrainingViewSet(viewsets.ReadOnlyModelViewSet):
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
    serializer_class = TnrisInstructorTypeSerializer
    http_method_names = ['get']

    def get_queryset(self):
        # get records using query
        queryset = TnrisInstructorType.objects.all()
        return queryset


# db view, not actual table; api endpoint for complete training records with instructor info
class CompleteForumTrainingViewSet(viewsets.ReadOnlyModelViewSet):
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
