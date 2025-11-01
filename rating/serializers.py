from rest_framework import serializers
from .models import VenueRating

class VenueRatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    bayesian_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = VenueRating
        fields = '__all__'

    def get_bayesian_rating(self, obj):
        # Calculate Bayesian rating for the venue of this rating
        from rating.models import VenueRating
        bayesian = VenueRating.update_bayesian_for_venue(obj.venue)
        br = bayesian.get('bayesian_rating') if isinstance(bayesian, dict) else None
        return round(br, 2) if br is not None else None
