from rest_framework import viewsets

from .models import CcrView, RemView, AreasView
from .serializers import (CollectionSerializer,
                         ResourceSerializer,
                         AreaSerializer)


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CollectionSerializer
    http_method_names = ['get']

    def get_queryset(self):
        # only return public collection records from the catalog
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
        queryset = CcrView.objects.filter(**args).order_by('collection_id')
        return queryset


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ResourceSerializer
    http_method_names = ['get']

    def get_queryset(self):
        args = {}
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
        queryset = RemView.objects.filter(**args)
        return queryset


class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AreaSerializer
    http_method_names = ['get']

    def get_queryset(self):
        args = {}
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
        queryset = AreasView.objects.filter(**args)
        return queryset
