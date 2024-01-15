from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination


from api.serializers import OrganizationSerializer, EventSerializer, EventCreateSerializer, SignupSerializer
from events.models import Organization, Event


class OrganizationCreateAPIView(CreateAPIView):
    """
    Create a new organization.
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    # permission_classes = [IsAuthenticated,]
    

class EventCreateView(CreateAPIView):
    """
    Create a new event.
    """
    serializer_class = EventCreateSerializer
    queryset = Event.objects.all()
    # permission_classes = [IsAuthenticated,]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#проверять, что запущен redis: redis-server
#проверять, что запущен celery: celery -A planner worker --loglevel=INFO
    

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
    # permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        queryset = Event.objects.all()
        return queryset
    

class SignupAPIView(CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny,]