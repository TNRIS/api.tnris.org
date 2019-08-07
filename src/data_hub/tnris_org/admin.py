from django.contrib import admin

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
    list_display = ('image_name', 'image_url', 'created')
    search_fields = ('image_name', 'image_url')


@admin.register(TnrisDocument)
class TnrisDocumentAdmin(admin.ModelAdmin):
    model = TnrisDocument
    form = DocumentForm
    ordering = ('document_name',)
    list_display = ('document_name', 'document_url', 'created')
    search_fields = ('document_name', 'document_url')


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
