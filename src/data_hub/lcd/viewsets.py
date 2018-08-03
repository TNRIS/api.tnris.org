from rest_framework import viewsets

from .models import CcrView
from .serializers import CollectionSerializer


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CcrView.objects.all()
    serializer_class = CollectionSerializer
    http_method_names = ['get']


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
