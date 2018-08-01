from django.contrib import admin

# from .filters import CollectionAgencyNameFilter, CollectionCountyFilter, \
#     CountyDropdownFilter
# from .forms import CollectionForm, ProductForm
from .models import (
    AgencyType,
    AreaType,
    BandRelate,
    BandType,
    CategoryRelate,
    CategoryType,
    Collection,
    CcrView,
    DataTypeRelate,
    DataType,
    EpsgRelate,
    EpsgType,
    FileTypeRelate,
    FileType,
    LicenseType,
    ResolutionRelate,
    ResolutionType,
    Resource,
    TemplateType,
    UseRelate,
    UseType
)

@admin.register(AgencyType)
class AgencyTypeAdmin(admin.ModelAdmin):
    model = AgencyType
    ordering = ('agency_name',)


@admin.register(AreaType)
class AreaTypeAdmin(admin.ModelAdmin):
    model = AreaType
    ordering = ('area_type_name',)


@admin.register(BandRelate)
class BandRelateAdmin(admin.ModelAdmin):
    model = BandRelate
    ordering = ('band_type_id',)


@admin.register(BandType)
class BandTypeAdmin(admin.ModelAdmin):
    model = BandType
    ordering = ('band_abbreviation',)


@admin.register(CategoryRelate)
class CategoryRelateAdmin(admin.ModelAdmin):
    model = CategoryRelate
    ordering = ('category_type_id',)


@admin.register(CategoryType)
class CategoryTypeAdmin(admin.ModelAdmin):
    model = CategoryType
    ordering = ('category',)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    model = Collection
    ordering = ('collection_id',)


@admin.register(CcrView)
class CcrViewAdmin(admin.ModelAdmin):
    model = CcrView
    ordering = ('name',)


@admin.register(DataTypeRelate)
class DataTypeRelateAdmin(admin.ModelAdmin):
    model = DataTypeRelate
    ordering = ('data_type_id',)


@admin.register(DataType)
class DataTypeAdmin(admin.ModelAdmin):
    model = DataType
    ordering = ('data_type',)


@admin.register(EpsgRelate)
class EpsgRelateAdmin(admin.ModelAdmin):
    model = EpsgRelate
    ordering = ('epsg_type_id',)


@admin.register(EpsgType)
class EpsgTypeAdmin(admin.ModelAdmin):
    model = EpsgType
    ordering = ('epsg_code',)


@admin.register(FileTypeRelate)
class FileTypeRelateAdmin(admin.ModelAdmin):
    model = FileTypeRelate
    ordering = ('file_type_id',)


@admin.register(FileType)
class FileTypeAdmin(admin.ModelAdmin):
    model = FileType
    ordering = ('file_type',)


@admin.register(LicenseType)
class LicenseTypeAdmin(admin.ModelAdmin):
    model = LicenseType
    ordering = ('license_abbreviation',)


@admin.register(ResolutionRelate)
class ResolutionRelateAdmin(admin.ModelAdmin):
    model = ResolutionRelate
    ordering = ('resolution_type_id',)


@admin.register(ResolutionType)
class ResolutionTypeAdmin(admin.ModelAdmin):
    model = ResolutionType
    ordering = ('resolution',)


@admin.register(TemplateType)
class TemplateTypeAdmin(admin.ModelAdmin):
    model = TemplateType
    ordering = ('template',)


@admin.register(UseType)
class UseTypeAdmin(admin.ModelAdmin):
    model = UseType
    ordering = ('use_type',)


@admin.register(UseRelate)
class UseRelateAdmin(admin.ModelAdmin):
    model = UseRelate
    ordering = ('use_type_id',)


# admin.site.register(AreaType, AreaTypeAdmin)
# admin.site.register(TemplateType, TemplateTypeAdmin)
# admin.site.register(LicenseType, LicenseTypeAdmin)
# admin.site.register(UseType, UseTypeAdmin)
# admin.site.register(FileType, FileTypeAdmin)
# admin.site.register(DataType, DataTypeAdmin)
# admin.site.register(ResolutionType, ResolutionTypeAdmin)
# admin.site.register(EpsgType, EpsgTypeAdmin)
# admin.site.register(CategoryType, CategoryTypeAdmin)
# admin.site.register(SourceType, SourceTypeAdmin)
# admin.site.register(BandType, BandTypeAdmin)
# admin.site.register(EpsgRelate, EpsgRelateAdmin)
# admin.site.register(Collection, CollectionAdmin)


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
