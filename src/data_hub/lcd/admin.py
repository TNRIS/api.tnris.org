from django.contrib import admin

# from .filters import CollectionAgencyNameFilter, CollectionCountyFilter, \
#     CountyDropdownFilter
from .forms import CollectionForm, ResourceForm
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
    ResourceType,
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
                       'delete_supplemental_report_url',
                       'lidar_breaklines_url',
                       'delete_lidar_breaklines_url',
                       'tile_index_url',
                       'delete_tile_index_url')
        }),
        ('Images', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('overview_image',
                       'delete_overview_image',
                       'thumbnail_image',
                       'delete_thumbnail_image',
                       'natural_image',
                       'delete_natural_image',
                       'urban_image',
                       'delete_urban_image')
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
        'name', 'collection_id', 'last_modified', 'public'
    )
    search_fields = ('name',)
    list_filter = (
        'public',
    )
    # remove default action 'delete_selected' so s3 files will be deleted by the
    # model's overridden delete method. also so user permissions don't have to be
    # handled. **No logical scenario calls for Collections to be bulk deleted
    def get_actions(self, request):
        actions = super(CollectionAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


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


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    model = Resource
    form = ResourceForm

    readonly_fields = ('resource',
                       'filesize',
                       'last_modified',
                       'collection_id',
                       'area_type_id',
                       'resource_type')

    ordering = ('collection_id',)
    list_display = (
        'collection_id', 'area_type_id', 'resource', 'resource_type', 'last_modified'
    )
    search_fields = ('collection_id', 'area_type_id', 'resource', 'resource_type')
    list_filter = (
        'collection_id',
        'area_type_id',
        'resource_type'
    )

    # override the /resource/add/ form
    def add_view(self,request,extra_context=None):
        # reset the declared_fields attr to be what it was on load
        self.form.declared_fields = self.original_declared_fields
        # set custom flag attributes for admin templates
        self.opts.resource_change_flag = False
        self.opts.resource_add_flag = True
        # turn off alternative save buttons
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(ResourceAdmin,self).add_view(request, extra_context=extra_context)

    # override the /resource/change/ form
    def change_view(self,request,object_id,extra_context=None):
        # clear declared_fields attr so 'collection' dropdown doesn't
        # appear on change form
        self.form.declared_fields = {}
        # set custom flag attributes for admin templates
        self.opts.resource_change_flag = True
        self.opts.resource_add_flag = False
        return super(ResourceAdmin,self).change_view(request,object_id)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # on initialization, set aside declared_fields attribute
        # so it can be re-applied based on form view
        self.original_declared_fields = self.form.declared_fields


@admin.register(TemplateType)
class TemplateTypeAdmin(admin.ModelAdmin):
    model = TemplateType
    ordering = ('template',)


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    model = ResourceType
    ordering = ('resource_type_name',)
    list_display = (
        'resource_type_name', 'resource_type_abbreviation'
    )


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
