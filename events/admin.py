from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model

from .models import Organization, Event, OrganizationEvent, EventOrganizers

User = get_user_model()
"""
Register the created models 
for their processing by the administrator
"""


class OrganizationInline(admin.TabularInline):
    model = Event.organizations.through


class EventsInline(admin.TabularInline):
    model = User.events.through


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'address', 'postcode')
    fields = ('title', 'description', ('address', 'postcode'))
    list_filter = ('title', 'postcode')
    search_fields = ('title',)
    ordering = ('title',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [OrganizationInline]
    list_display = ('title', 'description', 'display_organizations', 'date', 'get_image')
    readonly_fields = ('get_image',)
    list_filter = ('title', 'date')
    search_fields = ('title', 'organizations__title')
    ordering = ('title', 'date')

    def display_organizations(self, obj):
        # отображение организаторов 
        return ', '.join([org.title for org in obj.organizations.all()])
    
    display_organizations.short_description = 'Организаторы'

    def get_image(self, obj):
        # отображение изображения из модели в админке
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = 'Превью афиши'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [EventsInline]
    list_display = ('email', 'last_name', 'first_name', 'organization', 'phone_number', 'display_events')
    fields = ('email', ('first_name', 'last_name'), 'phone_number', 'organization', 'is_staff',)
    list_filter = ('organization',)
    search_fields = ('email', 'last_name')
    ordering = ('last_name', 'organization')

    def display_events(self, obj):
        # отображение организаторов 
        return ', '.join([org.title for org in obj.events.all()])
    
    display_events.short_description = 'Мероприятия'


admin.site.register(OrganizationEvent)

admin.site.register(EventOrganizers)