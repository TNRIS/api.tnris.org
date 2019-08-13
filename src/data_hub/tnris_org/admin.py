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
    TnrisInstructorType
)
from .filters import (
    TnrisForumTrainingYearFilter,
)


@admin.register(TnrisImage)
class TnrisImageAdmin(admin.ModelAdmin):
    model = TnrisImage
    form = ImageForm
    ordering = ('image_name',)
    list_display = ('image_name', 'image_url_link', 'tiny_preview', 'created')
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
            u'{0}<a style="cursor:pointer;border:solid 1px;padding:3px;" onclick="{1}Function();">COPY URL</a><input style="width:90%;margin-left:5px;" type="text" id="{2}" value="{3}" readonly>',
            js,
            htmlId,
            htmlId,
            obj.image_url
        )

    def tiny_preview(self, obj):
        return format_html(
            u'<a href="{0}" title="Click to view in full"><img style="max-width:100px;cursor:pointer;" src="{1}" /></a>',
            obj.image_url,
            obj.image_url
        )


@admin.register(TnrisDocument)
class TnrisDocumentAdmin(admin.ModelAdmin):
    model = TnrisDocument
    form = DocumentForm
    ordering = ('document_name',)
    list_display = ('document_name', 'document_url_link', 'tiny_preview', 'created')
    search_fields = ('document_name', 'document_url')

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
            u'{0}<a style="cursor:pointer;border:solid 1px;padding:3px;" onclick="{1}Function();">COPY URL</a><input style="width:90%;margin-left:5px;" type="text" id="{2}" value="{3}" readonly>',
            js,
            htmlId,
            htmlId,
            obj.document_url
        )

    def tiny_preview(self, obj):
        # tiny preview of .pdf files errors/breaks on page load when src is cached.
        # this means all tiny previews display on hard reload, but .pdfs don't on
        # normal reload. so, we append a current datetime query string to the request
        # so the browser recognizes each load as a new request and doesn't load the
        # cached version.
        no_cache = str(datetime.today())
        return format_html(
            u'<embed style="max-width: 120px;" src="{0}?d={1}"></embed>',
            obj.document_url,
            no_cache
        )


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
                    'public')
    search_fields = ('title')
    list_filter = (
        'instructor', 'registration_open', 'public'
    )


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
    search_fields = ('title')
    list_filter = (
        TnrisForumTrainingYearFilter,
        'registration_open',
        'public'
    )


@admin.register(TnrisInstructorType)
class TnrisInstructorTypeAdmin(admin.ModelAdmin):
    model = TnrisInstructorType
    form = TnrisInstructorTypeForm
    ordering = ('name',)
    list_display = ('name', 'company', 'headshot')
    search_fields = ('name', 'company')
