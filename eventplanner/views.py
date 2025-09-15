from rest_framework import viewsets, generics, permissions
from .models import CateringItem, Service, EventType, VenueImage
from .serializers import CateringItemSerializer, ServiceSerializer, EventTypeSerializer, VenueImageSerializer

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
		serializer.save(venue_id=venue_id)

class VenueImageViewSet(viewsets.ModelViewSet):
	queryset = VenueImage.objects.all()
	serializer_class = VenueImageSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	def get_queryset(self):
		venue_id = self.request.query_params.get('venue')
		qs = VenueImage.objects.all()
		if venue_id:
			qs = qs.filter(venue_id=venue_id)
		return qs
	def perform_create(self, serializer):
		venue_id = self.request.data.get('venue')
		serializer.save(venue_id=venue_id)
