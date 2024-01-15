from django.urls import path
from api.views import OrganizationCreateAPIView, EventCreateView, EventListView, SignupAPIView

app_name = 'api'

urlpatterns = [
    path('create_organization/', OrganizationCreateAPIView.as_view(), name='create_organization'),
    path('create_event/', EventCreateView.as_view(), name='create_event'),
    path('events/', EventListView.as_view(), name='events'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
]