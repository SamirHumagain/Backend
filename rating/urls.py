from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VenueRatingViewSet

router = DefaultRouter()
router.register(r'venue-ratings', VenueRatingViewSet, basename='venue-rating')

urlpatterns = [
    path('', include(router.urls)),
]
