from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Sum
from .models import VenueRating
from .serializers import VenueRatingSerializer
from venues.models import Venue

class VenueRatingViewSet(viewsets.ModelViewSet):
    def has_approved_reservation(self, user, venue):
        # Check if user has an approved reservation for any event at this venue
        from venues.models import Reservation, Event
        return Reservation.objects.filter(
            user=user,
            status='approved',
            event__venue=venue
        ).exists()
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
        user = self.request.user
        venue = serializer.validated_data['venue']
        if not self.has_approved_reservation(user, venue):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Booking approval is required to rate this venue.")
        rating_obj = serializer.save(user=user)
        # venue = rating_obj.venue

    def perform_update(self, serializer):
        user = self.request.user
        venue = serializer.validated_data['venue']
        if not self.has_approved_reservation(user, venue):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Booking approval is required to rate this venue.")
        rating_obj = serializer.save()

    def perform_destroy(self, instance):
        venue = instance.venue
        instance.delete()
    # Bayesian rating is calculated, but not saved to Venue model
