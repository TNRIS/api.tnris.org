from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from .models import TnrisTraining, TnrisForumTraining


class TnrisTrainingFiscalYearFilter(admin.SimpleListFilter):
    title = _('Fiscal Year')
    parameter_name = 'fiscal_year'

    def lookups(self, request, model_admin):
        # set aside empty string of years
        fiscal_years = []
        # function to determine which 4 digit fiscal year the 
        # datetime obj belongs to
        def append_fiscal_year(dt):
            if dt.month < 9:
                fiscal_years.append(dt.year)
            else:
                fiscal_years.append(dt.year + 1)
            return
        # get ordered, distinct list of state_date_time values
        start_dates = TnrisTraining.objects.order_by('start_date_time').values('start_date_time').distinct()
        # iterate distince list, run through function to determine
        # it's associated fiscal year
        for sd in start_dates:
            dt_obj = sd['start_date_time']
            append_fiscal_year(dt_obj)
        # create tuple list of dropdown values for filtering
        fy_list = list(sorted(set([(y, y) for y in fiscal_years])))
        return fy_list

    def queryset(self, request, queryset):
        if self.value():
            # create date range for jan-aug of this year
            jan = "%s-01-01" % self.value()
            aug = "%s-08-31" % self.value()
            # create date range for sept-dec last year
            last_year = int(self.value()) - 1
            sep = "%s-09-01" % last_year
            dec = "%s-12-31" % last_year
            # filter start_date_time to land in either range which makes
            # up the fiscal year
            return queryset.filter(Q(start_date_time__date__range=(jan, aug))|Q(start_date_time__range=(sep, dec)))


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