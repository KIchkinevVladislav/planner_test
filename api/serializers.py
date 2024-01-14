from rest_framework import serializers

from ivents.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer for model Organization
    """
    class Meta:
        model = Organization
        fields = ('title', 'description', 'address', 'postcode')