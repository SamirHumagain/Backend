from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Sum
from .models import VenueRating
from .serializers import VenueRatingSerializer
from venues.models import Venue

class VenueRatingViewSet(viewsets.ModelViewSet):
    queryset = VenueRating.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = VenueRatingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        venue_id = self.request.query_params.get('venue')
        if venue_id:
            queryset = queryset.filter(venue_id=venue_id)
        return queryset

    def perform_create(self, serializer):
        rating_obj = serializer.save(user=self.request.user)
        venue = rating_obj.venue
    # Bayesian rating is calculated, but not saved to Venue model

    def perform_update(self, serializer):
        rating_obj = serializer.save()
        venue = rating_obj.venue
    # Bayesian rating is calculated, but not saved to Venue model

    def perform_destroy(self, instance):
        venue = instance.venue
        instance.delete()
    # Bayesian rating is calculated, but not saved to Venue model
