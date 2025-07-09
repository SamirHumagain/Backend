from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Venue, Booking
from .serializers import VenueSerializer, BookingSerializer
from .permissions import IsVenueOwner

# Add venue
class AddVenueView(generics.CreateAPIView):
    serializer_class = VenueSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Edit / Delete venue
class UpdateDeleteVenueView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [permissions.IsAuthenticated, IsVenueOwner]
    parser_classes = [MultiPartParser, FormParser]

# View bookings for owner's venues
class OwnerBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(venue__owner=self.request.user)
