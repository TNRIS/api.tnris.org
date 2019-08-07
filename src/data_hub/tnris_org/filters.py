from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import TnrisForumTraining

class TnrisForumTrainingYearFilter(admin.SimpleListFilter):
    title = _('Forum Year')
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        start_dates = TnrisForumTraining.objects.values_list('start_date_time', 'start_date_time').order_by('start_date_time')
        years = list(sorted(set([(s.year, d.year) for (s, d) in start_dates]), key=lambda x: x[1]))
        return years

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(start_date_time__year=self.value())