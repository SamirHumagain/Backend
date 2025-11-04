from rest_framework import viewsets, generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import CateringItem, Service, EventType, VenueImage
from .serializers import CateringItemSerializer, ServiceSerializer, EventTypeSerializer, VenueImageSerializer
from venues.models import Venue

class CateringItemListCreateView(generics.ListCreateAPIView):
	serializer_class = CateringItemSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	def get_queryset(self):
		venue_id = self.kwargs.get('venue_id')
		return CateringItem.objects.filter(venue_id=venue_id)
	def perform_create(self, serializer):
		serializer.save(venue_id=self.kwargs.get('venue_id'))

class CateringItemDeleteView(generics.DestroyAPIView):
	queryset = CateringItem.objects.all()
	serializer_class = CateringItemSerializer
	permission_classes = [permissions.IsAuthenticated]

class ServiceViewSet(viewsets.ModelViewSet):
	queryset = Service.objects.all()
	serializer_class = ServiceSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	def get_queryset(self):
		venue_id = self.request.query_params.get('venue')
		qs = Service.objects.all()
		if venue_id:
			qs = qs.filter(venue_id=venue_id)
		return qs
	def perform_create(self, serializer):
		venue_id = self.request.data.get('venue')
		# Standard create for Service; no venue-image side effects here
		serializer.save(venue_id=venue_id)

class EventTypeViewSet(viewsets.ModelViewSet):
	queryset = EventType.objects.all()
	serializer_class = EventTypeSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	def get_queryset(self):
		venue_id = self.request.query_params.get('venue')
		qs = EventType.objects.all()
		if venue_id:
			qs = qs.filter(venue_id=venue_id)
		return qs
	def perform_create(self, serializer):
		venue_id = self.request.data.get('venue')
		# Standard create for EventType
		serializer.save(venue_id=venue_id)

class VenueImageViewSet(viewsets.ModelViewSet):
	queryset = VenueImage.objects.all()
	serializer_class = VenueImageSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	# Allow multipart/form-data file uploads
	parser_classes = [MultiPartParser, FormParser, JSONParser]
	def get_queryset(self):
		venue_id = self.request.query_params.get('venue')
		qs = VenueImage.objects.all()
		if venue_id:
			qs = qs.filter(venue_id=venue_id)
		return qs
	def perform_create(self, serializer):
		venue_id = self.request.data.get('venue')
		# Save the VenueImage instance
		instance = serializer.save(venue_id=venue_id)
		# After saving the VenueImage, update the Venue.image field to this image's absolute URL
		try:
			if venue_id and instance and getattr(instance, 'image', None):
				rel_url = instance.image.url if hasattr(instance.image, 'url') else str(instance.image)
				# Use request to build absolute URL
				image_url = self.request.build_absolute_uri(rel_url)
				Venue.objects.filter(id=venue_id).update(image=image_url)
		except Exception:
			# Do not fail the create if updating the venue image fails
			pass
