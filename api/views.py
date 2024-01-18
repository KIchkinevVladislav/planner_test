from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from django.contrib.auth import logout
from django.shortcuts import redirect

from api.serializers import (
    OrganizationSerializer, 
    EventSerializer, 
    EventCreateSerializer, 
    SignupSerializer, 
    DetailEventSerializer
)
from events.models import Organization, Event


class SignupAPIView(CreateAPIView):
    """
    User registration.
    """
    serializer_class = SignupSerializer
    permission_classes = [AllowAny,]


class OrganizationCreateAPIView(CreateAPIView):
    """
    Create a new organization.
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated,]
    

class EventCreateView(CreateAPIView):
    """
    Create a new event.
    """
    serializer_class = EventCreateSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated,]


class EventListView(ListAPIView):
    """
    Displaying a list of events:
    - filtering and sorting by date 
    - search by name 
    - limited pagination (default=10)
    """  
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['date']
    search_fields = ['title']
    ordering_fields = ['date']
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        queryset = Event.objects.all()
        return queryset
    

class EventDetailView(RetrieveAPIView):
    """
    Displaying an events.
    """ 
    queryset = Event.objects.all()
    serializer_class = DetailEventSerializer
    permission_classes = [IsAuthenticated,]    


def logout_view(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/api/v1/auth/login/')