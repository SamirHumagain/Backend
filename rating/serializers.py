
from rest_framework import serializers
from .models import VenueRating

class VenueRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueRating
        fields = ['id', 'venue', 'reservation', 'rating', 'review', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)
