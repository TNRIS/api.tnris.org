from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from lcd.models import CcrView
from lore.models import ChcView
from itertools import chain


class StaticSitemap(Sitemap):

    def items(self):
        return [
            'holodeck',
            'api_schema',
            'shopping_cart',
            'geofilter'
        ]

    def location(self, item):
        return reverse(item)


class CollectionSitemap(Sitemap):

    def items(self):
        return list(chain(CcrView.objects.filter(public=True).order_by('-acquisition_date'), ChcView.objects.filter(public=True).order_by('-acquisition_date')))

    def location(self, item):
        return reverse('collection', args=[item.collection_id])
