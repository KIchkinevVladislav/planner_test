from django.urls import path

from chat.views import home, new_group, join_group, leave_group, remove_group,  open_chat

app_name = 'chat'


urlpatterns = [
	path('', home, name='home'),
	path('new_group', new_group, name='new_group'),
	path('join_group/<uuid:uuid>', join_group, name='join_group'),
	path('leave_group/<uuid:uuid>', leave_group, name='leave_group'),
	path('remove_group/<uuid:uuid>', remove_group, name='remove_group'),
	path('open_chat/<uuid:uuid>', open_chat, name='open_chat'),
]