from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from events.models import Organization, Event

User = get_user_model()

class OrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer for model Organization
    """
    class Meta:
        model = Organization
        fields = ('id', 'title', 'description', 'address', 'postcode')

        
class EventSerializer(serializers.ModelSerializer):
    organizations = OrganizationSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'organizations', 'date', 'image')


class EventCreateSerializer(serializers.ModelSerializer):
    organizations = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        many=True,
        required=True
    )

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'organizations', 'date', 'image')


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