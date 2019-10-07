from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import PosterGallerySubmission


class PosterGallerySubmissionForumYearFilter(admin.SimpleListFilter):
    title = _('Forum Year')
    parameter_name = 'forum_year'

    def lookups(self, request, model_admin):
        created_dates = PosterGallerySubmission.objects.values_list('created', 'created').order_by('created')
        years = list(sorted(set([(s.year, d.year) for (s, d) in created_dates]), key=lambda x: x[1]))
        return years

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(created__year=self.value())