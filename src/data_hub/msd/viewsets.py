from rest_framework import viewsets
from rest_framework.response import Response

from .models import MsdView
from .serializers import (MapCollectionSerializer)

class MapCollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MapCollectionSerializer
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
        queryset = MsdView.objects.filter(**args)
        return queryset
