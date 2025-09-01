from rest_framework import serializers
from .models import Venue

class VenueOwnerDashboardSerializer(serializers.ModelSerializer):
    bookings_count = serializers.IntegerField()
    pending_requests = serializers.IntegerField()
    avg_rating = serializers.FloatField()

    class Meta:
        model = Venue
        fields = '__all__'
