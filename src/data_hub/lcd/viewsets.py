from rest_framework import viewsets

from .models import CcrView
from .serializers import CollectionSerializer


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = CcrView.objects.all()
    serializer_class = CollectionSerializer
    http_method_names = ['get']

    def get_queryset(self):
        print(self.request.query_params)
        args = {'public': True}
        null_list = ['null', 'Null', 'none', 'None']
        for field in self.request.query_params.keys():
            print(field)
            value = self.request.query_params.get(field)
            print(value)
            if value in null_list:
                value = None
            args[field] = value
        print(args)
        queryset = CcrView.objects.filter(**args)
        print(len(queryset))
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
