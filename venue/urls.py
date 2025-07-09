
from django.urls import path
from .views import AddVenueView, UpdateDeleteVenueView, OwnerBookingListView

urlpatterns = [
    path('owner/venues/add/', AddVenueView.as_view(), name='add-venue'),
    path('owner/venues/<int:pk>/', UpdateDeleteVenueView.as_view(), name='edit-delete-venue'),
    path('owner/bookings/', OwnerBookingListView.as_view(), name='owner-bookings'),
]
