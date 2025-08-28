from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (VenueViewSet, EventViewSet, ReservationViewSet, ServiceViewSet,
                    AdminDashboardStats, AdminUserList, AdminVenueList, AdminBookingList,
                    UserDashboardStats, UserBookingList, UserProfile, AdminAnalyticsStats,
                    OwnerVenueBookingList)
from .admin_user_detail import AdminUserDetail

router = DefaultRouter()
router.register(r'venues', VenueViewSet)
router.register(r'events', EventViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'services', ServiceViewSet)

urlpatterns = router.urls + [
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
]
