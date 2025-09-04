from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (VenueViewSet, EventViewSet, ReservationViewSet, ServiceViewSet,
                    EventTypeViewSet,
                    AdminDashboardStats, AdminUserList, AdminVenueList, AdminBookingList,
                    UserDashboardStats, UserBookingList, UserProfile, AdminAnalyticsStats,
                    OwnerVenueBookingList, haversine_api,
                    VenueRatingViewSet, FavoriteVenueViewSet, VenueImageViewSet)
from .views import CateringItemListCreateView, CateringItemDeleteView
from .admin_user_detail import AdminUserDetail


router = DefaultRouter()
router.register(r'venues', VenueViewSet)
router.register(r'events', EventViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'event-types', EventTypeViewSet)
router.register(r'venue-images', VenueImageViewSet)
router.register(r'venue-ratings', VenueRatingViewSet, basename='venue-rating')
router.register(r'favorite-venues', FavoriteVenueViewSet, basename='favorite-venue')

urlpatterns = [
    path('venues/owner/',
         VenueViewSet.as_view({'get': 'list'}),
         name='owner-venue-list'),
] + router.urls + [
    path('admin-dashboard/stats/', AdminDashboardStats.as_view(), name='admin-dashboard-stats'),
    path('admin-dashboard/users/', AdminUserList.as_view(), name='admin-dashboard-users'),
    path('admin-dashboard/venues/', AdminVenueList.as_view(), name='admin-dashboard-venues'),
    path('admin-dashboard/bookings/', AdminBookingList.as_view(), name='admin-dashboard-bookings'),
    path('user-dashboard/stats/', UserDashboardStats.as_view(), name='user-dashboard-stats'),
    path('user-dashboard/bookings/', UserBookingList.as_view(), name='user-dashboard-bookings'),
    path('user-dashboard/profile/', UserProfile.as_view(), name='user-dashboard-profile'),
    path('admin-dashboard/analytics/', AdminAnalyticsStats.as_view(), name='admin-dashboard-analytics'),
    path('venues/owner/bookings/', OwnerVenueBookingList.as_view(), name='owner-venue-bookings'),
    path('users/<int:user_id>/', AdminUserDetail.as_view(), name='admin-user-detail'),
    path('haversine/', haversine_api, name='haversine-api'),
    path('venues/<int:venue_id>/catering-items/', CateringItemListCreateView.as_view(), name='cateringitem-list-create'),
    path('catering-items/<int:pk>/', CateringItemDeleteView.as_view(), name='cateringitem-delete'),
]
