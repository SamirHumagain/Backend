from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    ServiceViewSet, EventTypeViewSet, VenueImageViewSet,
    CateringItemListCreateView, CateringItemDeleteView
)

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'event-types', EventTypeViewSet)
router.register(r'venue-images', VenueImageViewSet)

urlpatterns = [
    path('venues/<int:venue_id>/catering-items/', CateringItemListCreateView.as_view(), name='cateringitem-list-create'),
    path('catering-items/<int:pk>/', CateringItemDeleteView.as_view(), name='cateringitem-delete'),
] + router.urls
