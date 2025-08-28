
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db.models import Sum, Count, Avg
from datetime import datetime, timedelta

from .models import Venue, Event, Reservation, Service
from .serializers import VenueSerializer, EventSerializer, ReservationSerializer, ServiceSerializer, ReservationUserDashboardSerializer
from loginsignup.models import CustomUser

class AdminAnalyticsStats(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Revenue analytics

        today = datetime.today()
        first_day_this_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        first_day_last_month = (first_day_this_month - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day_last_month = first_day_this_month - timedelta(seconds=1)

        this_month_revenue = Reservation.objects.filter(
            reserved_at__gte=first_day_this_month, reserved_at__lte=today
        ).aggregate(total=Sum('event__venue__price'))['total'] or 0
        last_month_revenue = Reservation.objects.filter(
            reserved_at__gte=first_day_last_month, reserved_at__lte=last_day_last_month
        ).aggregate(total=Sum('event__venue__price'))['total'] or 0

        growth_rate = 0
        if last_month_revenue:
            growth_rate = ((this_month_revenue - last_month_revenue) / last_month_revenue) * 100

        # User engagement (dummy, replace with real metrics if available)
        daily_active_users = CustomUser.objects.filter(last_login__date=today).count()
        avg_session_duration = 12.34  # minutes, placeholder
        bounce_rate = 24.5  # percent, placeholder

        # Growth metrics (dummy, replace with real metrics if available)

        bookings_this_month = Reservation.objects.filter(reserved_at__gte=first_day_this_month, reserved_at__lte=today).count()
        venues_this_week = Venue.objects.filter(created_at__gte=today - timedelta(days=7)).count()
        customer_satisfaction = 92  # percent, placeholder

        return Response({
            'revenue': {
                'this_month': this_month_revenue,
                'last_month': last_month_revenue,
                'growth_rate': round(growth_rate, 2),
            },
            'user_engagement': {
                'daily_active_users': daily_active_users,
                'avg_session_duration': avg_session_duration,
                'bounce_rate': bounce_rate,
            },
            'growth_metrics': {
                'bookings_this_month': bookings_this_month,
                'venues_this_week': venues_this_week,
                'customer_satisfaction': customer_satisfaction,
            }
        })


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class ReservationViewSet(viewsets.ModelViewSet):

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        # Expecting event to be created first, then reservation
        event_id = request.data.get('event')
        if not event_id:
            return Response({'error': 'Event ID is required.'}, status=400)
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found.'}, status=404)

        # Check if another event exists for this venue and date
        # (excluding this event itself)
        same_venue_events = Event.objects.filter(venue=event.venue, date=event.date).exclude(id=event.id)
        if same_venue_events.exists():
            return Response({'error': 'This venue is already booked for the selected date.'}, status=400)

        # Also check if a reservation already exists for this event
        if Reservation.objects.filter(event=event).exists():
            return Response({'error': 'This event is already reserved.'}, status=400)

        return super().create(request, *args, **kwargs)

    # Custom actions for approval/rejection
    from rest_framework.decorators import action
    from rest_framework import status

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        reservation = self.get_object()
        # Only the owner of the venue can approve
        if reservation.event.venue.owner != request.user:
            return Response({'detail': 'Not allowed.'}, status=403)
        reservation.status = 'approved'
        reservation.save()
        return Response({'status': 'approved'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        reservation = self.get_object()
        # Only the owner of the venue can reject
        if reservation.event.venue.owner != request.user:
            return Response({'detail': 'Not allowed.'}, status=403)
        reservation.status = 'rejected'
        reservation.save()
        return Response({'status': 'rejected'})

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AdminDashboardStats(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_users = CustomUser.objects.count()
        total_venues = Venue.objects.count()
        total_bookings = Reservation.objects.count()
        total_revenue = 0  # Placeholder, implement revenue logic if needed
        pending_approvals = Venue.objects.filter(status='pending').count()
        active_events = 0  # Placeholder, implement if you have events
        return Response({
            'totalUsers': total_users,
            'totalVenues': total_venues,
            'totalBookings': total_bookings,
            'totalRevenue': total_revenue,
            'pendingApprovals': pending_approvals,
            'activeEvents': active_events,
        })

class AdminUserList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = CustomUser.objects.all().values('id', 'name', 'email', 'user_type', 'date_joined', 'is_active')
        return Response(list(users))

class AdminVenueList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        venues = Venue.objects.all().values()
        return Response(list(venues))

class AdminBookingList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        bookings = Reservation.objects.all().values()
        return Response(list(bookings))

class UserDashboardStats(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        total_bookings = Reservation.objects.filter(user=user).count()
        # Add more stats as needed
        return Response({
            'totalBookings': total_bookings,
        })

class UserBookingList(APIView):
    permission_classes = [IsAuthenticated]

    from .serializers import ReservationUserDashboardSerializer

    def get(self, request):
        user = request.user
        bookings = Reservation.objects.filter(user=user)
        serializer = ReservationUserDashboardSerializer(bookings, many=True)
        return Response(serializer.data)

class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'user_type': user.user_type,
            'date_joined': user.date_joined,
            'is_active': user.is_active,
        })
