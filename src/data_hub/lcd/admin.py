from django.contrib import admin

# from .filters import CollectionAgencyNameFilter, CollectionCountyFilter, \
#     CountyDropdownFilter
from .forms import CollectionForm, ResourceForm, ImageForm, XlargeSupplementalForm
from .models import (
    AreaType,
    CategoryRelate,
    CategoryType,
    Collection,
    CcrView,
    EpsgRelate,
    EpsgType,
    FileTypeRelate,
    FileType,
    Image,
    LicenseType,
    ResolutionRelate,
    ResolutionType,
    Resource,
    ResourceType,
    ResourceTypeRelate,
    SourceType,
    TemplateType,
    UseRelate,
    UseType,
    XlargeSupplemental
)

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
    list_display = ('category', 'filter_name')


class ImageInlineAdmin(admin.StackedInline):
    classes = ('grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-open',)
    model = Image
    form = ImageForm
    extra = 0


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    model = Collection
    form = CollectionForm
    fieldsets = (
        ('Collection Information', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('name',
                       'template_type_id',
                       'acquisition_date',
                       # 'short_description',
                       'description',
                       # 'authoritative',
                       # 'known_issues',
                       # 'coverage_extent',
                       # 'tags',
                       'source_type_id',
                       'partners',
                       'license_type_id',
                       'thumbnail_image',
                       'esri_open_data_id',
                       'public'),
        }),
        ('Links', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('wms_link',
                       'popup_link',
                       'supplemental_report_url',
                       # 'carto_map_id',
                       'delete_supplemental_report_url',
                       'lidar_breaklines_url',
                       'delete_lidar_breaklines_url',
                       'lidar_buildings_url',
                       'delete_lidar_buildings_url',
                       'tile_index_url',
                       'delete_tile_index_url')
        }),
        ('Lookup/Relate Associations', {
            'classes': ('grp-collapse grp-closed',),
            'fields': (('projections', 'categories'),
                       ('file_types', 'resolutions'),
                       # ('uses', 'counties'))
                       ('counties',))
        })
    )
    inlines = [ImageInlineAdmin]
    ordering = ('name',)
    list_display = (
        'disp_name', 'collection_id', 'last_modified', 'public'
    )
    search_fields = ('name', 'collection_id', 'acquisition_date')
    list_filter = (
        'public', 'template_type_id'
    )

    # set aside acqusition_date year for list display
    def disp_name(self, collection):
        if collection.acquisition_date is not None and collection.template_type_id is not None and collection.template_type_id.template != 'outside-entity':
            year = collection.acquisition_date.split("-")[0] + " "
        else:
            year = ""
        return year + collection.name
    disp_name.short_description = 'Collection Display Name'

    # remove default action 'delete_selected' so s3 files will be deleted by the
    # model's overridden delete method. also so user permissions don't have to be
    # handled. **No logical scenario calls for Collections to be bulk deleted
    def get_actions(self, request):
        actions = super(CollectionAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    # handle the thumbnail image attribute if inline images were changed
    def save_formset(self, request, form, formset, change):
        super(CollectionAdmin, self).save_formset(request, form, formset, change)
        # only for the Image table inlines
        if formset.model == Image:
            obj = formset.instance
            # query for number of images saved for this collection
            total_images = Image.objects.filter(collection_id=obj.collection_id)
            # if none exist, clear thumbnail image reference
            if len(total_images) == 0:
                obj.thumbnail_image = ""
            # if only one image exists, use it for the thumbnail
            elif len(total_images) == 1:
                obj.thumbnail_image = total_images[0].image_url
            obj.save()

    def get_form(self, request, obj=None, **kwargs):
        # if username is 'admin' or user is part of 'Master of Resources' group
        # then show the Public field. otherwise, hide it
        if str(request.user) == 'admin' or 'Master of Resources' in str(request.user.groups.all()):
            if 'public' not in self.fieldsets[0][1]['fields']:
                self.fieldsets[0][1]['fields'] = self.fieldsets[0][1]['fields'] + ('public',)
        else:
            self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if x != 'public')
        return super(CollectionAdmin,self).get_form(request, obj, **kwargs)


# views not compiled from joined tables. not managed in admin console
# @admin.register(CcrView)
# class CcrViewAdmin(admin.ModelAdmin):
#     model = CcrView
#     ordering = ('name',)


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
                       'resource_type_id')

    ordering = ('collection_id',)
    list_display = (
        'disp_name', 'area_type_id', 'resource', 'resource_type_id', 'last_modified'
    )
    search_fields = ('collection_id__name', 'area_type_id__area_type_name', 'resource', 'resource_type_id__resource_type_name')
    list_filter = (
        'collection_id',
        'area_type_id',
        'resource_type_id'
    )

    # set aside acqusition_date year for list display
    def disp_name(self, resource):
        if resource.collection_id.acquisition_date is not None and resource.collection_id.template_type_id.template != 'outside-entity':
            year = resource.collection_id.acquisition_date.split("-")[0] + " "
        else:
            year = ""
        return year + resource.collection_id.name
    disp_name.short_description = 'Collection Display Name'

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


# Resource Type Relate table managed through 'Resource' form as s3 zipfiles are
# required to create/manage relate records
# @admin.register(ResourceTypeRelate)
# class ResourceTypeRelateAdmin(admin.ModelAdmin):
#     model = ResourceTypeRelate
#     ordering = ('collection_id',)


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    model = ResourceType
    ordering = ('resource_type_name',)
    list_display = (
        'resource_type_name', 'resource_type_abbreviation'
    )


@admin.register(SourceType)
class SourceTypeAdmin(admin.ModelAdmin):
    model = SourceType
    ordering = ('source_name',)
    list_display = ('source_name', 'source_abbreviation')


@admin.register(TemplateType)
class TemplateTypeAdmin(admin.ModelAdmin):
    model = TemplateType
    ordering = ('template',)
    list_display = ('template', 'filter_name')


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

@admin.register(XlargeSupplemental)
class XlargeSupplementalAdmin(admin.ModelAdmin):
    model = XlargeSupplemental
    form = XlargeSupplementalForm

    # override the /xlargesupplemental/add/ form
    def add_view(self,request,extra_context=None):
        # reset the declared_fields attr to be what it was on load
        self.form.declared_fields = self.original_declared_fields
        # set custom flag attributes for admin templates
        self.opts.xlargesupplemental_change_flag = False
        self.opts.xlargesupplemental_add_flag = True
        # turn off alternative save buttons
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(XlargeSupplementalAdmin,self).add_view(request, extra_context=extra_context)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # on initialization, set aside declared_fields attribute
        # so it can be re-applied based on form view
        self.original_declared_fields = self.form.declared_fields
