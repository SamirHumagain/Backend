
# All imports at the very top
from rest_framework import serializers
from .models import Venue, Event, Reservation, Service, VenueRating, FavoriteVenue, VenueImage
from loginsignup.owner_detail_serializer import OwnerDetailSerializer

# --- Serializers for VenueRating and FavoriteVenue ---

class VenueSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()
    bookings_count = serializers.IntegerField(required=False)
    pending_requests = serializers.IntegerField(required=False)
    avg_rating = serializers.SerializerMethodField(read_only=True)
    services = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Venue
        fields = '__all__'

    def get_services(self, obj):
        from .serializers import ServiceSerializer
        return ServiceSerializer(obj.services.all(), many=True).data

    def get_images(self, obj):
        from .serializers import VenueImageSerializer
        return VenueImageSerializer(obj.images.all(), many=True).data

    def get_avg_rating(self, obj):
        avg = getattr(obj, "avg_rating", None)
        if avg is None:
            return None
        return round(avg, 2)

    def get_rating(self, obj):
        ratings = getattr(obj, 'ratings', None)
        if ratings is None:
            return 0
        ratings_qs = ratings.all()
        if ratings_qs.exists():
            return round(sum(r.rating for r in ratings_qs) / ratings_qs.count(), 2)
        return 0
class VenueRatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    venue = serializers.PrimaryKeyRelatedField(queryset=Venue.objects.all())

    class Meta:
        model = VenueRating
        fields = ['id', 'user', 'venue', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class FavoriteVenueSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    venue = serializers.PrimaryKeyRelatedField(queryset=Venue.objects.all())

    class Meta:
        model = FavoriteVenue
        fields = ['id', 'user', 'venue', 'added_at']
        read_only_fields = ['id', 'user', 'added_at']

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
            return obj.event.venue.location_name or obj.event.venue.name
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

# VenueImage serializer
class VenueImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueImage
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

