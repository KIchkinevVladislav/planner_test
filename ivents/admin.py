from django.contrib import admin

from .models import Organization
"""
Register the created models 
for their processing by the administrator
"""

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'address', 'postcode')
    fields = ('title', 'description', ('address', 'postcode'))
    list_filter = ('title', 'postcode')
    search_fields = ('title',)
    ordering = ('title',)