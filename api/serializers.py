from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from events.models import Organization, Event, EventOrganizers

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for create model User
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }
        

    def create(self, validated_data):
        password = validated_data['password']
        
        try:
            validate_password(password=password)
        except ValidationError as err:
            raise serializers.ValidationError({'password': err.messages})
        
        user = User(email=validated_data['email'])
        user.set_password(password)
        user.save()

        return user
    

class OrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer for model Organization
    """
    class Meta:
        model = Organization
        fields = ('id', 'title', 'description', 'address', 'postcode')

        
class EventCreateSerializer(serializers.ModelSerializer):
    organizations = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        many=True,
        required=True
    )

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'organizations', 'date', 'image')
    

class EventSerializer(serializers.ModelSerializer):
    organizations = OrganizationSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'organizations', 'date', 'image')


class OneEventSerializer(serializers.ModelSerializer):
    organizers = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'date', 'image', 'organizers')

    def get_organizers(self, obj):
        organizers_data = self.get_organizers_data(obj.id)
        return organizers_data

    def get_organizers_data(self, event_id):
        event_organizers = EventOrganizers.objects.filter(event_id=event_id)
        organizers_data = {}

        for eo in event_organizers:
            organization_id = eo.user_id.organization_id
            user_data = {
                'id': eo.user_id.id,
                'email': eo.user_id.email,
                'first_name': eo.user_id.first_name,
                'last_name': eo.user_id.last_name,
                'phone_number': eo.user_id.phone_number,
            }

            if organization_id not in organizers_data:
                organization_serializer = OrganizationSerializer(eo.user_id.organization)
                organization_data = organization_serializer.data
                organization_data['address'] = f"{organization_data['address']}, {organization_data['postcode']}"
                del organization_data['postcode']
                organizers_data[organization_id] = {
                    'organization': organization_data,
                    'users': [user_data],
                }
            else:
                organizers_data[organization_id]['users'].append(user_data)

        return list(organizers_data.values())