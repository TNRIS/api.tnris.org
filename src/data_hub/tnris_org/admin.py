from django.contrib import admin

# Register your models here.
from .forms import ImageForm, DocForm
from .models import (
    TnrisImageUrl,
    TnrisDocUrl
)


@admin.register(TnrisImageUrl)
class TnrisImageUrlAdmin(admin.ModelAdmin):
    model = TnrisImageUrl
    form = ImageForm
    ordering = ('image_name',)
    list_display = ('image_name', 'image_url')


@admin.register(TnrisDocUrl)
class TnrisDocUrlAdmin(admin.ModelAdmin):
    model = TnrisDocUrl
    form = DocForm
    ordering = ('doc_name',)
    list_display = ('doc_name', 'doc_url')
