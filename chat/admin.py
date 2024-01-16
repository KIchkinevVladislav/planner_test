from django.contrib import admin

from .models import Group, Message
"""
Register the created models 
for their processing by the administrator
"""
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'timestamp', 'content', 'group')
    readonly_fields = ('author', 'timestamp', 'content', 'group')
    list_filter = ('group', 'author')
    search_fields = ('author', 'content')
    ordering = ('timestamp',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'display_members',)
    readonly_fields = ('uuid', 'members',)
    list_filter = ('uuid',)
    ordering = ('uuid',)

    def display_members(self, obj):
        # отображение участников чата
        return ', '.join([mem.get_full_name() for mem in obj.members.all()])
    
    display_members.short_description = 'Участники'