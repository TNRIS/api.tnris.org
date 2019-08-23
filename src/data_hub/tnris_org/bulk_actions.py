# 
# BULK ACTIONS
# used in admin console list display
# 

def close_registration(modeladmin, request, queryset):
    queryset.update(registration_open=False)
close_registration.short_description = "Close Registration"

def open_registration(modeladmin, request, queryset):
    queryset.update(registration_open=True)
open_registration.short_description = "Open Registration"

def close_to_public(modeladmin, request, queryset):
    queryset.update(public=False)
close_to_public.short_description = "Close to Public on website"

def open_to_public(modeladmin, request, queryset):
    queryset.update(public=True)
open_to_public.short_description = "Open to Public on website"