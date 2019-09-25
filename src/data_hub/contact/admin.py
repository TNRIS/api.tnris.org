from django.contrib import admin
from .models import (
    EmailTemplate,
    GeneralContact
)
# Register your models here.
@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    model = EmailTemplate


@admin.register(GeneralContact)
class GeneralContactAdmin(admin.ModelAdmin):
    model = GeneralContact