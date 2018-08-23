from rest_framework import viewsets
from rest_framework.response import Response

from .models import County, CountyRelate, Product, Collection
from .serializers import (CountySerializer, ProductSerializer)
from rest_framework.permissions import AllowAny
import boto3


class CountyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = County.objects.all()
    serializer_class = CountySerializer
    http_method_names = ['get']


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    http_method_names = ['get']

    def get_queryset(self):
        fips = self.request.query_params.get('countyFips')

        if fips:
            county = County.objects.get(fips=fips)
            collections = (
                CountyRelate.objects.filter(county=county.id)
                .select_related("collection")
            )

            public_recs = Collection.objects.filter(public=True)

            queryset = (Product.objects.filter(collection_id__in=collections.values_list("collection"))
                .filter(collection_id__in=public_recs.values_list("id")).select_related("collection"))

        else:
            queryset = Product.objects.select_related("collection")

        return queryset

class MapserverViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):
        client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )
        keys = []
        def get_mapfiles(token):
            if token == '':
                response = client.list_objects_v2(
                    Bucket='tnris-ls4',
                    Prefix='mapfiles/'
                )
            else:
                response = client.list_objects_v2(
                    Bucket='tnris-ls4',
                    Prefix='mapfiles/',
                    ContinuationToken=token
                )
            goods = [x['Key'] for x in response['Contents'] if x['Key'] != 'mapfiles/']
            keys.extend(goods)
            if 'NextContinuationToken' in response.keys():
                get_mapfiles(response['NextContinuationToken'])
            else:
                return keys
        all_keys = get_mapfiles('')
        for key in all_keys:
            key_obj = {}
            pos = all_keys.index(key)
            name = key.replace('mapfiles/', '').replace('.map', '')
            key_obj['name'] = name
            key_obj['label'] = name.replace("_", " ").title()
            key_obj['wms'] = 'http://mapserver.tnris.org/wms/?map=/' + key

            if len(name.split("_")) == 4:
                key_obj['org'] = 'county'
                one = name.split("_")[0]
                two = name.split("_")[1]
                three = name.split("_")[2]
                four = name.split("_")[3]

                key_obj['county'] = one
                key_obj['agency'] = two
                key_obj['year'] = three
                key_obj['type'] = four
                key_obj['mission'] = 'n/a'

            elif len(name.split("_")) == 3:
                key_obj['org'] = 'multi'
                one = name.split("_")[0]
                two = name.split("_")[1]
                three = name.split("_")[2]

                key_obj['county'] = 'MULTIPLE'
                key_obj['agency'] = one
                key_obj['year'] = ''
                key_obj['type'] = three
                key_obj['mission'] = two

            all_keys[pos] = key_obj
        return Response(all_keys)
