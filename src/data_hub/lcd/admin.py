from django.contrib import admin

# from .filters import CollectionAgencyNameFilter, CollectionCountyFilter, \
#     CountyDropdownFilter
# from .forms import CollectionForm, ProductForm
from .models import (
    ZippedByAreaType,
    StateType,
    CountyType,
    QuadType,
    QQuadType,
    UsngType,
    TemplateType,
    LicenseType,
    UseType,
    FileType,
    DataType,
    ResolutionType,
    EpsgType,
    CategoryType,
    SourceType,
    BandType,
    EpsgRelate,
    Collection
)


class ZippedByAreaTypeAdmin(admin.ModelAdmin):
    model = ZippedByAreaType
    ordering = ('zipped_by_area_type_name',)


class StateTypeAdmin(admin.ModelAdmin):
    model = StateType
    ordering = ('state_fips', 'state_name',)


class CountyTypeAdmin(admin.ModelAdmin):
    model = CountyType
    ordering = ('county_name',)


class QuadTypeAdmin(admin.ModelAdmin):
    model = QuadType
    ordering = ('usgs_doq_name',)


class QQuadTypeAdmin(admin.ModelAdmin):
    model = QQuadType
    ordering = ('q_quad_name',)


class UsngTypeAdmin(admin.ModelAdmin):
    model = UsngType
    ordering = ('usng_name',)


class TemplateTypeAdmin(admin.ModelAdmin):
    model = TemplateType
    ordering = ('template',)


class LicenseTypeAdmin(admin.ModelAdmin):
    model = LicenseType
    ordering = ('license_abbreviation',)


class UseTypeAdmin(admin.ModelAdmin):
    model = UseType
    ordering = ('use_type',)


class FileTypeAdmin(admin.ModelAdmin):
    model = FileType
    ordering = ('file_type',)


class DataTypeAdmin(admin.ModelAdmin):
    model = DataType
    ordering = ('data_type',)


class ResolutionTypeAdmin(admin.ModelAdmin):
    model = ResolutionType
    ordering = ('resolution',)


class EpsgTypeAdmin(admin.ModelAdmin):
    model = EpsgType
    ordering = ('epsg_code',)


class CategoryTypeAdmin(admin.ModelAdmin):
    model = CategoryType
    ordering = ('category',)


class SourceTypeAdmin(admin.ModelAdmin):
    model = SourceType
    ordering = ('source_name',)


class BandTypeAdmin(admin.ModelAdmin):
    model = BandType
    ordering = ('band_abbreviation',)


class EpsgRelateAdmin(admin.ModelAdmin):
    model = EpsgRelate
    ordering = ('epsg_type_id',)


class CollectionAdmin(admin.ModelAdmin):
    model = Collection

admin.site.register(ZippedByAreaType, ZippedByAreaTypeAdmin)
admin.site.register(StateType, StateTypeAdmin)
admin.site.register(CountyType, CountyTypeAdmin)
admin.site.register(QuadType, QuadTypeAdmin)
admin.site.register(QQuadType, QQuadTypeAdmin)
admin.site.register(UsngType, UsngTypeAdmin)
admin.site.register(TemplateType, TemplateTypeAdmin)
admin.site.register(LicenseType, LicenseTypeAdmin)
admin.site.register(UseType, UseTypeAdmin)
admin.site.register(FileType, FileTypeAdmin)
admin.site.register(DataType, DataTypeAdmin)
admin.site.register(ResolutionType, ResolutionTypeAdmin)
admin.site.register(EpsgType, EpsgTypeAdmin)
admin.site.register(CategoryType, CategoryTypeAdmin)
admin.site.register(SourceType, SourceTypeAdmin)
admin.site.register(BandType, BandTypeAdmin)
admin.site.register(EpsgRelate, EpsgRelateAdmin)
admin.site.register(Collection, CollectionAdmin)


#
# class PhotoIndexInlineAdmin(admin.StackedInline):
#     classes = ('grp-collapse grp-closed',)
#     inline_classes = ('grp-collapse grp-closed',)
#     model = PhotoIndex
#     extra = 0
#
#
# class CountyRelateInlineAdmin(admin.StackedInline):
#     classes = ('grp-collapse grp-closed',)
#     inline_classes = ('grp-collapse grp-closed',)
#     model = CountyRelate
#     extra = 0
#     ordering = ('county__name',)
#
#
# class CollectionAdmin(admin.ModelAdmin):
#     model = Collection
#     form = CollectionForm
#     fieldsets = (
#         ('Collection Information', {
#             'fields': ('collection', 'agency', 'from_date', 'to_date', 'counties', 'public'),
#         }),
#         ('Remarks', {
#             'fields': ('remarks',)
#         })
#     )
#     inlines = [PhotoIndexInlineAdmin, LineIndexInlineAdmin,
#                MicroficheIndexInlineAdmin, ProductInlineAdmin]
#     list_display = (
#         'collection', 'agency', 'from_date', 'to_date', 'county_names', 'public'
#     )
#     ordering = ('agency__name', 'from_date')
#     search_fields = ('collection',)
#     list_filter = (
#         'public',
#         CollectionAgencyNameFilter,
#         CollectionCountyFilter
#     )
#
#     def county_names(self, collection):
#         county_relates = (
#             CountyRelate.objects.filter(collection=collection)
#                 .select_related('county').values_list("county__name")
#         )
#         counties = sorted([c[0] for c in county_relates])
#         return "{}".format(", ".join(name for name in counties))
#
#     county_names.short_description = "Counties in Collection"
#
#
# # Register your models here.
# class CountyAdmin(admin.ModelAdmin):
#     list_filter = (
#         ('name', CountyDropdownFilter),
#     )
#     list_per_page = 25
#     ordering = ('name',)
#     list_display = ('name', 'fips')
#     # search_fields = ['name', 'fips']
