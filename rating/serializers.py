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
        return round(bayesian['bayesian_rating'], 2)
