
# All imports at the very top
from rest_framework import serializers
from .models import Venue, Event, Reservation, Service

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Event
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'  # status is now included

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class EventNestedSerializer(serializers.ModelSerializer):
    venue = VenueSerializer()
    class Meta:
        model = Event
        fields = ['id', 'name', 'date', 'venue']

class ReservationUserDashboardSerializer(serializers.ModelSerializer):
    event = EventNestedSerializer()
    class Meta:
        model = Reservation
        fields = ['id', 'status', 'reserved_at', 'event']

