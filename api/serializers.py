from rest_framework import serializers

from events.models import Organization, Event, Organization_Event


class OrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer for model Organization
    """
    class Meta:
        model = Organization
        fields = ('title', 'description', 'address', 'postcode')

        
class EventSerializer(serializers.ModelSerializer):
    organizations = OrganizationSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('title', 'description', 'organizations', 'date', 'image')


class EventCreateSerializer(serializers.ModelSerializer):
    organizations = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        many=True,
        required=True
    )

    class Meta:
        model = Event
        fields = ('title', 'description', 'organizations', 'date', 'image')