from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import CcrView, RemView, AreasView
from .serializers import (
    CollectionSerializer,
    ResourceSerializer,
    AreaSerializer,
)

class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve TNRIS dataset collection metadata and information
    """
    
    """
    Below we are using DRF Filtering to handle
    filtering, sorting, and keyword search,
    documentation found here:
    https://www.django-rest-framework.org/api-guide/filtering/
    """
    
    # define the fields available to search
    search_fields = [
        'name',
        'acquisition_date',
        '@description',
        '@counties',
        'source_name',
        'source_abbreviation',
        'partners',
        'oe_service_names'
    ]
    # define the fields available to sort
    ordering_fields = ['name', 'acquisition_date']
    # add search and ordering to the filter backends so we
    # can filter the api with the frontend sort and search
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)

    serializer_class = CollectionSerializer
    http_method_names = ['get']

    def get_queryset(self):
        # only return public collection records from the catalog
        args = {'public': True}
        null_list = ['null', 'Null', 'none', 'None']
        # create argument object of query clauses
        for field in self.request.query_params.keys():
            if field not in ['limit', 'offset', 'ordering', 'search']:
                value = self.request.query_params.get(field)
                # convert null queries
                if value in null_list:
                    value = None
                args[field] = value
        # get records using query
        queryset = CcrView.objects.filter(**args).order_by('collection_id')
        return queryset


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve TNRIS dataset collection resources/downloads
    """
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
        queryset = RemView.objects.filter(**args).order_by('resource_id')
        return queryset


class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve TNRIS resource/download areas
    """
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
        queryset = AreasView.objects.filter(**args).order_by('area_type_id')
        return queryset
