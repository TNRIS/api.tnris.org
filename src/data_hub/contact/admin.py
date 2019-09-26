from django.contrib import admin
from .models import (
    EmailTemplate,
    GeneralContact
)
# Register your models here.
@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    model = EmailTemplate
    list_display = (
        'email_template_type',
        'email_template_subject',
        'email_template_id'
    )
    readonly_fields = ('email_template_id',)
    ordering = ('email_template_type',)


@admin.register(GeneralContact)
class GeneralContactAdmin(admin.ModelAdmin):
    model = GeneralContact
    list_display = (
        'name',
        'email',
        'phone',
        'address',
        'organization',
        'industry',
        'question_or_comments',
        'created'
    )
    ordering = ('-created',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields