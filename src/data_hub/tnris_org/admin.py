from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .forms import (
    ImageForm,
    DocumentForm,
    TnrisTrainingForm,
    TnrisForumTrainingForm
)
from .models import (
    TnrisImage,
    TnrisDocument,
    TnrisTraining,
    TnrisForumTraining
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
        return format_html(
            u'<embed sandbox style="max-width: 120px;" src="{0}"></embed>',
            obj.document_url
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
    search_fields = ('title', 'instructor')
    list_filter = (
        'instructor', 'registration_open', 'public'
    )


@admin.register(TnrisForumTraining)
class TnrisForumTrainingAdmin(admin.ModelAdmin):
    model = TnrisForumTraining
    form = TnrisForumTrainingForm
    ordering = ('title',)
    list_display = ('title',
                    'instructor',
                    'start_date_time',
                    'end_date_time',
                    'registration_open',
                    'public',
                    'year')
    search_fields = ('title', 'instructor')
    list_filter = (
        TnrisForumTrainingYearFilter,
        'registration_open',
        'public'
    )
