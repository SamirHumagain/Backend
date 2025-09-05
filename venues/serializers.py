
# All imports at the very top
from rest_framework import serializers
from .models import Venue, Event, Reservation, VenueRating, FavoriteVenue
from loginsignup.owner_detail_serializer import OwnerDetailSerializer

# --- Serializers for VenueRating and FavoriteVenue ---

class VenueSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    bookings_count = serializers.IntegerField(required=False)
    pending_requests = serializers.IntegerField(required=False)
    avg_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Venue
        fields = '__all__'

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

# EventSerializer for Event model
class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Event
        fields = '__all__'

# ReservationSerializer for Reservation model
class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    event = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Reservation
        fields = '__all__'

# ReservationUserDashboardSerializer for Reservation model
class ReservationUserDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

# AdminBookingSerializer for Reservation model
class AdminBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

# FavoriteVenueSerializer for FavoriteVenue model
class FavoriteVenueSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = FavoriteVenue
        fields = '__all__'

# VenueRatingSerializer for VenueRating model
class VenueRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueRating
        fields = '__all__'
# All imports at the very top
from rest_framework import serializers
from .models import Venue, Event, Reservation


from loginsignup.owner_detail_serializer import OwnerDetailSerializer



class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Event
        fields = '__all__'


        fields = ['id', 'name', 'date', 'venue']




