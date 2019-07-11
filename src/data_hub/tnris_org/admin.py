from django.contrib import admin

# Register your models here.
from .forms import ImageForm, DocumentForm
from .models import (
    TnrisImage,
    TnrisDocument
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
