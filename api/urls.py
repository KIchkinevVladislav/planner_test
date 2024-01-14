from django.urls import path

from api.views import OrganizationCreateAPIView

app_name = 'api'

urlpatterns = [
    path('create_organization/', OrganizationCreateAPIView.as_view(), name='create_organization'),
]