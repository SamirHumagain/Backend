# Import serializers from rest_framework
from rest_framework import serializers
from .models import Reservation

# Admin Booking Serializer for richer admin dashboard data
class AdminBookingSerializer(serializers.ModelSerializer):
    venue_name = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    customer_email = serializers.SerializerMethodField()
    event_date = serializers.SerializerMethodField()
    guests = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = [
            'id', 'status', 'reserved_at',
            'venue_name', 'customer_name', 'customer_email',
            'event_date', 'guests', 'amount',
        ]

    def get_venue_name(self, obj):
        try:
            return obj.event.venue.name
        except Exception:
            return None

    def get_customer_name(self, obj):
        try:
            return obj.user.name
        except Exception:
            return None

    def get_customer_email(self, obj):
        try:
            return obj.user.email
        except Exception:
            return None

    def get_event_date(self, obj):
        try:
            return obj.event.date
        except Exception:
            return None

    def get_guests(self, obj):
        try:
            return obj.event.guests
        except Exception:
            return None

    def get_amount(self, obj):
        try:
            return obj.event.venue.price
        except Exception:
            return None
# All imports at the very top
from rest_framework import serializers
from .models import Venue, Event, Reservation, Service


from loginsignup.owner_detail_serializer import OwnerDetailSerializer

class VenueSerializer(serializers.ModelSerializer):
    owner = OwnerDetailSerializer(read_only=True)
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


# Move EventNestedSerializer above ReservationOwnerDashboardSerializer so it is defined before use
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

class ReservationOwnerDashboardSerializer(serializers.ModelSerializer):
    event = EventNestedSerializer()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ['id', 'status', 'reserved_at', 'event', 'user']

    def get_user(self, obj):
        user = getattr(obj, 'user', None)
        if user:
            return {
                'id': user.id,
                'name': user.name,
                'email': user.email,
            }
        return None

