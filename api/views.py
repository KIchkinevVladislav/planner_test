from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.serializers import OrganizationSerializer, EventSerializer, EventCreateSerializer
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