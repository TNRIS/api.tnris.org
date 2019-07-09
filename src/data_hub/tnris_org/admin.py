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
    ordering = ('category',)
    list_display = ('category', 'filter_name')
