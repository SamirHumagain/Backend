
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

    class Meta:
        model = Venue
        fields = '__all__'
        # Add owner_details to output
        extra_fields = ['owner_details']

    def get_bayesian_rating(self, obj):
        from rating.models import VenueRating
        bayesian = VenueRating.update_bayesian_for_venue(obj)
        return round(bayesian['bayesian_rating'], 2)

class EventSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Reservation
        fields = '__all__'

class AdminBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class FavoriteVenueSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = FavoriteVenue
        fields = '__all__'
        model = Reservation

        fields = '__all__'



# FavoriteVenueSerializer for FavoriteVenue model

