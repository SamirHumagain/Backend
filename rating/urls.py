
from django.urls import path
from .views import VenueRatingCreateView, VenueRatingListView

urlpatterns = [
    path('add/', VenueRatingCreateView.as_view(), name='add-rating'),
    path('venue/<int:venue_id>/', VenueRatingListView.as_view(), name='venue-ratings'),
]
