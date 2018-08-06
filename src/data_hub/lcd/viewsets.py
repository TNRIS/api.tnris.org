from rest_framework import viewsets

from .models import CcrView, Resource, AcdcView
from .serializers import (CollectionSerializer,
                         ResourceSerializer,
                         AreaSerializer)


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = CcrView.objects.all()
    serializer_class = CollectionSerializer
    http_method_names = ['get']

    def get_queryset(self):
        args = {'public': True}
        null_list = ['null', 'Null', 'none', 'None']
        for field in self.request.query_params.keys():
            value = self.request.query_params.get(field)
            if value in null_list:
                value = None
            args[field] = value
        print(args)
        queryset = CcrView.objects.filter(**args)
        return queryset

class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    http_method_names = ['get']

    def get_queryset(self):
        args = {}
        null_list = ['null', 'Null', 'none', 'None']
        for field in self.request.query_params.keys():
            value = self.request.query_params.get(field)
            if value in null_list:
                value = None
            args[field] = value
        print(args)
        queryset = Resource.objects.filter(**args)
        return queryset

class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = AcdcView.objects.all()
    serializer_class = AreaSerializer
    http_method_names = ['get']

    def get_queryset(self):
        args = {}
        null_list = ['null', 'Null', 'none', 'None']
        for field in self.request.query_params.keys():
            value = self.request.query_params.get(field)
            if value in null_list:
                value = None
            args[field] = value
        print(args)
        queryset = AcdcView.objects.filter(**args)
        return queryset



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
