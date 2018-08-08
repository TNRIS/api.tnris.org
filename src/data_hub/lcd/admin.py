from django.contrib import admin

# from .filters import CollectionAgencyNameFilter, CollectionCountyFilter, \
#     CountyDropdownFilter
from .forms import CollectionForm
from .models import (
    AcdcView,
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


# views not compiled from joined tables. not managed in admin console
# @admin.register(AcdcView)
# class AcdcViewAdmin(admin.ModelAdmin):
#     model = AcdcView
#     ordering = ('name',)


@admin.register(AgencyType)
class AgencyTypeAdmin(admin.ModelAdmin):
    model = AgencyType
    ordering = ('agency_name',)


# AreaType is solidified as statewide, counties, quads, qquads, & national grid
# not managed in admin console as it shouldn't be changing
# @admin.register(AreaType)
# class AreaTypeAdmin(admin.ModelAdmin):
#     model = AreaType
#     ordering = ('area_type_name',)


# Relate tables managed through 'Collection' form as collection records are
# required to create/manage relate records
# @admin.register(BandRelate)
# class BandRelateAdmin(admin.ModelAdmin):
#     model = BandRelate
#     ordering = ('band_type_id',)


@admin.register(BandType)
class BandTypeAdmin(admin.ModelAdmin):
    model = BandType
    ordering = ('band_abbreviation',)


# Relate tables managed through 'Collection' form as collection records are
# required to create/manage relate records
# @admin.register(CategoryRelate)
# class CategoryRelateAdmin(admin.ModelAdmin):
#     model = CategoryRelate
#     ordering = ('category_type_id',)


@admin.register(CategoryType)
class CategoryTypeAdmin(admin.ModelAdmin):
    model = CategoryType
    ordering = ('category',)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    model = Collection
    form = CollectionForm
    fieldsets = (
        ('Collection Information', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('name',
                       'acquisition_date',
                       'short_description',
                       'description',
                       'source',
                       'authoritative',
                       'public',
                       'known_issues',
                       'coverage_extent',
                       'tags',
                       'agency_type_id',
                       'license_type_id',
                       'template_type_id'),
        }),
        ('Links', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('carto_map_id',
                       'wms_link',
                       'popup_link',
                       'supplemental_report_url',
                       'lidar_breaklines_url',
                       'tile_index_url',)
        }),
        ('Images', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('overview_image',
                       'thumbnail_image',
                       'natural_image',
                       'urban_image')
        }),
        ('Lookup/Relate Associations', {
            'classes': ('grp-collapse grp-closed',),
            'fields': (('bands', 'categories'),
                       ('data_types', 'projections'),
                       ('file_types', 'resolutions'),
                       'uses')
        })
    )
    ordering = ('name',)
    list_display = (
        'name', 'public'
    )
    search_fields = ('name',)
    list_filter = (
        'public',
        # CollectionAgencyNameFilter,
        # CollectionCountyFilter
    )


# views not compiled from joined tables. not managed in admin console
# @admin.register(CcrView)
# class CcrViewAdmin(admin.ModelAdmin):
#     model = CcrView
#     ordering = ('name',)


# Relate tables managed through 'Collection' form as collection records are
# required to create/manage relate records
# @admin.register(DataTypeRelate)
# class DataTypeRelateAdmin(admin.ModelAdmin):
#     model = DataTypeRelate
#     ordering = ('data_type_id',)


@admin.register(DataType)
class DataTypeAdmin(admin.ModelAdmin):
    model = DataType
    ordering = ('data_type',)


# Relate tables managed through 'Collection' form as collection records are
# required to create/manage relate records
# @admin.register(EpsgRelate)
# class EpsgRelateAdmin(admin.ModelAdmin):
#     model = EpsgRelate
#     ordering = ('epsg_type_id',)


@admin.register(EpsgType)
class EpsgTypeAdmin(admin.ModelAdmin):
    model = EpsgType
    ordering = ('epsg_code',)


# Relate tables managed through 'Collection' form as collection records are
# required to create/manage relate records
# @admin.register(FileTypeRelate)
# class FileTypeRelateAdmin(admin.ModelAdmin):
#     model = FileTypeRelate
#     ordering = ('file_type_id',)


@admin.register(FileType)
class FileTypeAdmin(admin.ModelAdmin):
    model = FileType
    ordering = ('file_type',)


@admin.register(LicenseType)
class LicenseTypeAdmin(admin.ModelAdmin):
    model = LicenseType
    ordering = ('license_abbreviation',)


# Relate tables managed through 'Collection' form as collection records are
# required to create/manage relate records
# @admin.register(ResolutionRelate)
# class ResolutionRelateAdmin(admin.ModelAdmin):
#     model = ResolutionRelate
#     ordering = ('resolution_type_id',)


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


# Relate tables managed through 'Collection' form as collection records are
# required to create/manage relate records
# @admin.register(UseRelate)
# class UseRelateAdmin(admin.ModelAdmin):
#     model = UseRelate
#     ordering = ('use_type_id',)

#
# -------------------------------------
#
# EVEYTHING BELOW THIS LINE CAN BE DELETED.
# Reminents from data concierge
#
# -------------------------------------
#
#

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
