
# All imports at the very top
from rest_framework import serializers
from .models import Venue, Event, Reservation, FavoriteVenue
from loginsignup.owner_detail_serializer import OwnerDetailSerializer

# --- Serializers for VenueRating and FavoriteVenue ---

class VenueSerializer(serializers.ModelSerializer):
    bookings_count = serializers.IntegerField(required=False)
    pending_requests = serializers.IntegerField(required=False)
    bayesian_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Venue
        fields = '__all__'

    def get_bayesian_rating(self, obj):
        from rating.models import VenueRating
        bayesian = VenueRating.update_bayesian_for_venue(obj)
        return round(bayesian['bayesian_rating'], 2)

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




