from rest_framework import viewsets

from .models import CcrView, RemView, AcdcView, RuaView
from .serializers import (CollectionSerializer,
                         ResourceSerializer,
                         AreaSerializer,
                         RuaSerializer)


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
        print(args)
        # get records using query
        queryset = CcrView.objects.filter(**args)
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
        print(args)
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
        print(args)
        # get records using query
        queryset = AcdcView.objects.filter(**args)
        return queryset


class RuaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RuaSerializer
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
        print(args)
        # get records using query
        queryset = RuaView.objects.filter(**args)
        return queryset


#
# -------------------------------------
#
# EVEYTHING BELOW THIS LINE CAN BE DELETED.
# Reminents from data concierge
#
# -------------------------------------
#
#

# class ProductViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = ProductSerializer
#     http_method_names = ['get']
#
#     def get_queryset(self):
#         fips = self.request.query_params.get('countyFips')
#
#         if fips:
#             county = County.objects.get(fips=fips)
#             collections = (
#                 CountyRelate.objects.filter(county=county.id)
#                 .select_related("collection")
#             )
#
#             public_recs = Collection.objects.filter(public=True)
#
#             queryset = (Product.objects.filter(collection_id__in=collections.values_list("collection"))
#                 .filter(collection_id__in=public_recs.values_list("id")).select_related("collection"))
#
#         else:
#             queryset = Product.objects.select_related("collection")
#
#         return queryset
