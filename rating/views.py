from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import VenueRating
from .serializers import VenueRatingSerializer

class VenueRatingCreateView(generics.CreateAPIView):
    queryset = VenueRating.objects.all()
    serializer_class = VenueRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class VenueRatingListView(generics.ListAPIView):
    serializer_class = VenueRatingSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        venue_id = self.kwargs['venue_id']
        return VenueRating.objects.filter(venue_id=venue_id)
