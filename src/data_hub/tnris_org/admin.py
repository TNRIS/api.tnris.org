from django.contrib import admin
from django.utils.html import format_html
from datetime import datetime

# Register your models here.
from .forms import (
    ImageForm,
    DocumentForm,
    TnrisTrainingForm,
    TnrisForumTrainingForm,
    TnrisInstructorTypeForm
)
from .models import (
    TnrisImage,
    TnrisDocument,
    TnrisTraining,
    TnrisForumTraining,
    TnrisInstructorType,
    TnrisGioCalendarEvent,
    TrainingCategory
)
from .filters import (
    TnrisTrainingFiscalYearFilter,
    TnrisForumTrainingYearFilter,
)
from .bulk_actions import (
    close_registration,
    open_registration,
    close_to_public,
    open_to_public
)


@admin.register(TnrisImage)
class TnrisImageAdmin(admin.ModelAdmin):
    model = TnrisImage
    form = ImageForm
    ordering = ('image_name',)
    list_display = ('image_name', 'image_url_link', 'tiny_preview', 'carousel', 'created')
    search_fields = ('image_name', 'image_url')

    def image_url_link(self, obj):
        htmlId = "i" + str(obj.image_id).replace("-","")
        js = """
        <script type="text/javascript">
            function {id}Function() {{
                var copyText = document.getElementById("{id}");
                copyText.select();
                document.execCommand("copy");
            }}
        </script>
        <style>.field-image_url_link{{width:60%;}}</style>
        """.replace('{id}', htmlId)
        js = format_html(js)
        return format_html(
            u'{0}<div style="margin-bottom:10px;"><a style="cursor:pointer;border:solid 1px;padding:3px;" onclick="{1}Function();">COPY URL</a></div><div><input style="width:90%;" type="text" id="{2}" value="{3}" readonly></input></div>',
            js,
            htmlId,
            htmlId,
            obj.image_url.replace('https://tnris-org-static.s3.amazonaws.com/', 'https://cdn.tnris.org/')
        )

    def tiny_preview(self, obj):
        return format_html(
            u'<a href="{0}" title="Click to view in full"><img style="max-width:100px;cursor:pointer;" src="{1}" /></a>',
            obj.image_url.replace('https://tnris-org-static.s3.amazonaws.com/', 'https://cdn.tnris.org/'),
            obj.image_url.replace('https://tnris-org-static.s3.amazonaws.com/', 'https://cdn.tnris.org/')
        )


@admin.register(TnrisDocument)
class TnrisDocumentAdmin(admin.ModelAdmin):
    model = TnrisDocument
    form = DocumentForm
    ordering = ('document_name',)
    list_display = ('document_name', 'document_url_link', 'created', 'sgm_note', 'comm_note')
    search_fields = ('document_name', 'document_url')
    fieldsets = (
        ('Upload File -- or -- Enter URL', {
            # 'classes': ('grp-collapse', 'grp-open'),
            'fields': ('document_file',
                       'document_url',
                       )
        }),
        ('Name & Type', {
            # 'classes': ('grp-collapse', 'grp-open',),
            'fields': ('document_name',
                       'sgm_note',
                       'comm_note',
                       )
        }),
    )

    def document_url_link(self, obj):
        htmlId = "i" + str(obj.document_id).replace("-","")
        js = """
        <script type="text/javascript">
            function {id}Function() {{
                var copyText = document.getElementById("{id}");
                copyText.select();
                document.execCommand("copy");
            }}
        </script>
        <style>.field-document_url_link{{width:60%;}}</style>
        """.replace('{id}', htmlId)
        js = format_html(js)
        return format_html(
            u'{0}<div style="margin-bottom:10px;"><a style="cursor:pointer;border:solid 1px;padding:3px;" onclick="{1}Function();">COPY URL</a></div><div><input style="width:90%;" type="text" id="{2}" value="{3}" readonly></input></div>',
            js,
            htmlId,
            htmlId,
            obj.document_url.replace('https://tnris-org-static.s3.amazonaws.com/', 'https://cdn.tnris.org/')
        )

    # use the model's delete method as means to fire the s3 file
    # deletion at time of records being deleted from the list_display actions
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


@admin.register(TnrisTraining)
class TnrisTrainingAdmin(admin.ModelAdmin):
    model = TnrisTraining
    form = TnrisTrainingForm
    ordering = ('title',)
    list_display = ('title',
                    'instructor',
                    'start_date_time',
                    'end_date_time',
                    'registration_open',
                    'public',
                    'fiscal_year')
    search_fields = ('title', 'description')
    list_filter = (
        TnrisTrainingFiscalYearFilter,
        'instructor',
        'registration_open',
        'public'
    )
    # bulk update actions
    actions = [
        close_registration,
        open_registration,
        close_to_public,
        open_to_public
    ]


@admin.register(TnrisForumTraining)
class TnrisForumTrainingAdmin(admin.ModelAdmin):
    model = TnrisForumTraining
    form = TnrisForumTrainingForm
    ordering = ('title',)
    list_display = ('title',
                    'start_date_time',
                    'end_date_time',
                    'registration_open',
                    'public',
                    'year')
    search_fields = (
        'title',
        'description',
        'tnris_forum_training_ids__instructor_relate_id__name',
        'tnris_forum_training_ids__instructor_relate_id__company',
        'tnris_forum_training_ids__instructor_relate_id__bio'
    )
    list_filter = (
        TnrisForumTrainingYearFilter,
        'registration_open',
        'public'
    )
    # bulk update actions
    actions = [
        close_registration,
        open_registration,
        close_to_public,
        open_to_public
    ]


@admin.register(TnrisInstructorType)
class TnrisInstructorTypeAdmin(admin.ModelAdmin):
    model = TnrisInstructorType
    form = TnrisInstructorTypeForm
    ordering = ('name',)
    list_display = ('name', 'company', 'headshot_url')
    search_fields = ('name', 'company')

    def headshot_url(self, obj):
        url = obj.headshot
        if obj.headshot is not None:
            url = url.replace('https://tnris-org-static.s3.amazonaws.com/', 'https://cdn.tnris.org/')
        return url


@admin.register(TrainingCategory)
class TrainingCategoryAdmin(admin.ModelAdmin):
    model = TrainingCategory
    ordering = ('training_category',)
    list_display = ('training_category',)
    search_fields = ('training_category_id', 'training_category')


@admin.register(TnrisGioCalendarEvent)
class TnrisGioCalendarEventAdmin(admin.ModelAdmin):
    model = TnrisGioCalendarEvent
    ordering = ('start_date',)
    list_display = ('title',
                    'location',
                    'start_date',
                    'end_date',
                    'start_time',
                    'end_time',
                    'public')
    search_fields = ('title', 'location', 'start_date', 'end_date')

    fieldsets = (
        ('Basic Info', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': ('title',
                       'location',
                       'start_date',
                       'end_date',
                       'start_time',
                       'end_time'),
        }),
        ('More Details', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('short_description',
                       'event_url',
                       'community_meeting',
                       'community_meeting_agenda_url',
                       'solutions_group_meeting',
                       'public'),
        }),
        ('Address Specifics', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('street_address',
                       'city',
                       'state',
                       'zipcode'),
        })
    )
