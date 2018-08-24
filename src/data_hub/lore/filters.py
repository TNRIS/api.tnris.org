# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_admin_listfilter_dropdown.filters import (DropdownFilter,
                                                      RelatedDropdownFilter)

from .models import (Agency, Collection, County, CountyRelate)


class RelatedCountyDropdownFilter(RelatedDropdownFilter):
    def __init__(self, *args, **kwargs):
        RelatedDropdownFilter.__init__(self, *args, **kwargs)
        self.title = 'County'
        self.lookup_choices = sorted(self.lookup_choices)


class CountyDropdownFilter(DropdownFilter):
    def __init__(self, *args, **kwargs):
        DropdownFilter.__init__(self, *args, **kwargs)
        self.title = 'County'
        self.lookup_choices = sorted(self.lookup_choices)


class CollectionAgencyNameFilter(admin.SimpleListFilter):
    title = _('Agency Name')
    parameter_name = 'agency'

    def lookups(self, request, model_admin):
        agencies = Agency.objects.values_list('name', 'name').order_by('name')
        return (agencies)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(agency__name=self.value())


class CollectionCountyFilter(admin.SimpleListFilter):
    title = 'County'
    parameter_name = 'collection'

    def lookups(self, request, model_admin):
        agency = request.GET.getlist('agency')
        if agency:
            ag = Agency.objects.get(name=agency[0])
            county_relates = (
                CountyRelate.objects.select_related('county')
                .select_related("collection")
                .filter(collection__agency=ag)
                .order_by("county__name")
                .values_list("county__id", "county__name")
            )
            return (
                (c[0], c[1]) for c in sorted(set(county_relates), key=lambda x: x[1]))
        counties = County.objects.all().order_by('name')
        return ((county.id, county.name) for county in counties)

    def queryset(self, request, queryset):
        agency = request.GET.getlist('agency')
        if self.value():
            county_collections = CountyRelate.objects.filter(
                county_id=uuid.UUID(self.value())).values_list("collection")
            if agency:
                ag = Agency.objects.get(name=agency[0])
                results = (Collection.objects.filter(id__in=county_collections)
                           .filter(agency=ag))
                if results.count() > 0:
                    return results
                return Collection.objects.filter(agency=ag)
            return Collection.objects.filter(id__in=county_collections)
