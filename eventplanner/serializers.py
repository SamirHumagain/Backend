from rest_framework import serializers
from .models import CateringItem, Service, EventType, VenueImage

class CateringItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CateringItem
        fields = ['id', 'name', 'price', 'type', 'venue']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ['id', 'name', 'label', 'price', 'venue']

class VenueImageSerializer(serializers.ModelSerializer):
    # Use ImageField so DRF will accept uploaded files and return URL in response
    image = serializers.ImageField(use_url=True, required=True)

    class Meta:
        model = VenueImage
        fields = '__all__'
