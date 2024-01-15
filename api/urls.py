from django.urls import path
from api.views import (
    OrganizationCreateAPIView, 
    EventCreateView, 
    EventListView, 
    SignupAPIView, 
    logout_view
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'api'

urlpatterns = [
    path('create_organization/', OrganizationCreateAPIView.as_view(), name='create_organization'),
    path('create_event/', EventCreateView.as_view(), name='create_event'),
    path('events/', EventListView.as_view(), name='events'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('auth/logout/', logout_view, name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]