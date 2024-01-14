from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Organization, Event, Organization_Event
"""
Register the created models 
for their processing by the administrator
"""
admin.site.register(Organization_Event)

class OrganizationInline(admin.TabularInline):
    model = Event.organizations.through


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'address', 'postcode')
    fields = ('title', 'description', ('address', 'postcode'))
    list_filter = ('title', 'postcode')
    search_fields = ('title',)
    ordering = ('title',)


@admin.register(Event)
class IventAdmin(admin.ModelAdmin):
    inlines = [OrganizationInline]
    list_display = ('title', 'description', 'display_organizations', 'date', 'get_image')
    # fields = ('title', 'description', 'display_organizations', 'image', 'date')
    readonly_fields = ('get_image',)
    list_filter = ('title', 'date')
    search_fields = ('title', 'organizations__title')
    ordering = ('title', 'date')

    def display_organizations(self, obj):
        # отображение организаторов 
        return ', '.join([org.title for org in obj.organizations.all()])
    
    display_organizations.short_description = 'Организаторы'

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = 'Превью афиши'