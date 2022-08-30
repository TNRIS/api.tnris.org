import operator
from functools import reduce
from django.db.models import Q
from rest_framework import viewsets
from rest_framework import filters
from rest_framework_gis.filters import InBBoxFilter
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django_filters.rest_framework import DjangoFilterBackend

from .models import CatalogCollectionMetaView, CcrView, RemView, AreasView, ResourceType
from .serializers import (
    CatalogCollectionMetaSerializer,
    CollectionSerializer,
    ResourceSerializer,
    AreaSerializer,
    ResourceTypeSerializer
)

def getArgs(self):
    # Helper function to get arguments based on query parameters.
    # Note: Ignores fields limit, search, ordering and offset as they are special query parameters.
    args = {}
    null_list = ['null', 'Null', 'none', 'None']
    # create argument object of query clauses
    for field in self.request.query_params.keys():
        if field != 'limit' and field != 'offset' and field != 'search' and field != 'ordering':
            value = self.request.query_params.get(field)
            # convert null queries
            if value in null_list:
                value = None
            args[field] = value
    return args

class CatalogCollectionMetaViewSet(viewsets.ReadOnlyModelViewSet):
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
    search_fields = (
        'name',
        'description',
        'counties',
        'source_name',
        'source_abbreviation',
    )
    # define the fields available to sort
    ordering_fields = ['name', 'acquisition_date']
    # add search and ordering to the filter backends so we
    # can filter the api with the frontend sort and search
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, InBBoxFilter)
    bbox_filter_field = 'the_geom'
    bbox_filter_include_overlapping = True
    serializer_class = CatalogCollectionMetaSerializer
    http_method_names = ['get']

    def get_queryset(self):
        # only return public collection records from the catalog
        args = {'public': True}
        null_list = ['null', 'Null', 'none', 'None']
        #join_OR_conditions stores all OR clauses
        # create argument object of query clauses
        join_OR_conditions = []
        
        search = self.request.GET.get('search')
        search_vector = SearchVector(*self.search_fields)
        search_query = SearchQuery(search)
        for field in self.request.query_params.keys():
            if field not in ['limit', 'offset', 'ordering', 'search', 'in_bbox']:
                value = self.request.query_params.get(field)
                # convert null queries
                if value in null_list:
                    value = None
                
                args[field] = value
                
                # if field is CSV and one of designated OR fields
                or_fields = ["category__icontains", "availability__icontains", "file_type__icontains"]
                if "," in value and field in or_fields:
                    #split values
                    values = value.split(",")
                    #create objs array to fill from csv params
                    objs = []
                    #for each value in CSV Param, append
                    for v in values:
                        obj = {}
                        obj[field]=v
                        objs.append(obj)
                    #split into Q objects joined by bitwise "OR"
                    conditions = reduce(operator.or_, [Q(**o) for o in objs])
                    del args[field]
                    join_OR_conditions.append(conditions)
        # get records using query
        if search:
            queryset = CatalogCollectionMetaView.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(*join_OR_conditions,**args, search=search_query).order_by('-rank')
        else:
            queryset = CatalogCollectionMetaView.objects.filter(*join_OR_conditions,**args)
        return queryset

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

class ResourceTypeViewSet(viewsets.ReadOnlyModelViewSet): 
    """
    Retrieve TNRIS resource types
    """

    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ['resource_type_id', 'resource_type_name', 'resource_type_abbreviation', 'resource_type_category__category_name']
    ordering_fields = ['resource_type_name', 'created', 'last_modified', 'resource_type_category__category_name']
    serializer_class = ResourceTypeSerializer
    http_method_names = ['get']
    
    def get_queryset(self):
        args = getArgs(self)

        return ResourceType.objects.filter(**args).order_by('resource_type_id')

class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve TNRIS dataset collection resources/downloads
    """
    serializer_class = ResourceSerializer
    http_method_names = ['get']

    def get_queryset(self):
        args = getArgs(self)
        # get records using query
        return RemView.objects.filter(**args).order_by('resource_id')


class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve TNRIS resource/download areas
    """
    serializer_class = AreaSerializer
    http_method_names = ['get']

    def get_queryset(self):
        args = getArgs(self)
        # get records using query
        return AreasView.objects.filter(**args).order_by('area_type_id')
