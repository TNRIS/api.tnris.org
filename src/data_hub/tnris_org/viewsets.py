from rest_framework import viewsets
from rest_framework.response import Response

from .models import TnrisTraining, TnrisForumTraining
from .serializers import (TnrisTrainingSerializer, TnrisForumTrainingSerializer)

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
