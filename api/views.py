from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.serializers import OrganizationSerializer
from events.models import Organization


class OrganizationCreateAPIView(CreateAPIView):
    """
    Create a new organization.
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    # permission_classes = [IsAuthenticated,]