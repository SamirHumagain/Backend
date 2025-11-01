
from rest_framework import serializers
from .models import Venue, Event, Reservation, FavoriteVenue
from eventplanner.serializers import VenueImageSerializer
from loginsignup.owner_detail_serializer import OwnerDetailSerializer


class VenueSerializer(serializers.ModelSerializer):
    bookings_count = serializers.IntegerField(required=False)
    pending_requests = serializers.IntegerField(required=False)
    bayesian_rating = serializers.SerializerMethodField(read_only=True)
    images = VenueImageSerializer(many=True, read_only=True)
    owner_details = OwnerDetailSerializer(source='owner', read_only=True)
    num_ratings = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Venue
        fields = '__all__'
        # Add owner_details and num_ratings to output
        extra_fields = ['owner_details', 'num_ratings']

    def get_bayesian_rating(self, obj):
        from rating.models import VenueRating
        bayesian = VenueRating.update_bayesian_for_venue(obj)
        return round(bayesian['bayesian_rating'], 2)

    def get_num_ratings(self, obj):
        # Return the number of ratings for this venue
        return obj.ratings.count() if hasattr(obj, 'ratings') else 0

class EventSerializer(serializers.ModelSerializer):
    venue = VenueSerializer(read_only=True)
    organizer = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Event
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    event = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Reservation
        fields = '__all__'

class ReservationUserDashboardSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    # include nested user details so owner dashboard can show requester name/email
    user = OwnerDetailSerializer(read_only=True)
    class Meta:
        model = Reservation
        fields = '__all__'

class AdminBookingSerializer(serializers.ModelSerializer):
    # Provide extra read-only fields that the admin frontend expects
    event = EventSerializer(read_only=True)
    customer_name = serializers.SerializerMethodField(read_only=True)
    venue_name = serializers.SerializerMethodField(read_only=True)
    event_date = serializers.SerializerMethodField(read_only=True)
    amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Reservation
        # include core reservation fields plus convenient read-only fields
        fields = [
            'id',
            'user',
            'event',
            'status',
            'reserved_at',
            'customer_name',
            'venue_name',
            'event_date',
            'amount',
        ]

    def get_customer_name(self, obj):
        # prefer name, fall back to email
        user = getattr(obj, 'user', None)
        if not user:
            return None
        return getattr(user, 'name', None) or getattr(user, 'email', '')

    def get_venue_name(self, obj):
        try:
            return obj.event.venue.name
        except Exception:
            return None

    def get_event_date(self, obj):
        try:
            return obj.event.date
        except Exception:
            return None

    def get_amount(self, obj):
        try:
            return obj.event.venue.price
        except Exception:
            return 0

class FavoriteVenueSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = FavoriteVenue
        fields = '__all__'



# FavoriteVenueSerializer for FavoriteVenue model

