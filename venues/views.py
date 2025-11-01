from rest_framework import permissions
from rest_framework import serializers
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
import math
import logging

from django.core.mail import send_mail
from django.conf import settings

# Haversine formula utility
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# API endpoint for Haversine distance
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def haversine_api(request):
    try:
        lat1 = float(request.query_params.get('lat1'))
        lon1 = float(request.query_params.get('lon1'))
        lat2 = float(request.query_params.get('lat2'))
        lon2 = float(request.query_params.get('lon2'))
    except (TypeError, ValueError):
        return Response({'error': 'Invalid or missing parameters.'}, status=400)
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    return Response({'distance_km': round(distance, 3)})
# Ensure IsAuthenticated is imported at the top
from rest_framework.permissions import IsAuthenticated
# Ensure APIView is imported at the top
from rest_framework.views import APIView
class OwnerVenueBookingList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all reservations for venues owned by this user
        owner = request.user
        venues = Venue.objects.filter(owner=owner)
        events = Event.objects.filter(venue__in=venues)
        bookings = Reservation.objects.filter(event__in=events).select_related('event', 'user')
        from .serializers import ReservationUserDashboardSerializer
        serializer = ReservationUserDashboardSerializer(bookings, many=True)
        return Response(serializer.data)

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db.models import Sum, Count, Avg
from datetime import datetime, timedelta

from .models import Venue, Event, Reservation, FavoriteVenue
from .serializers import VenueSerializer, EventSerializer, ReservationSerializer, ReservationUserDashboardSerializer, AdminBookingSerializer
# Restore VenueRatingViewSet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.response import Response

from .serializers import FavoriteVenueSerializer

# Recommended venues API
from rating.models import VenueRating
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
@api_view(['GET'])
@permission_classes([AllowAny])
def recommended_venues(request):
    venues = Venue.objects.all()
    # Calculate Bayesian rating for each venue
    venue_list = []
    for venue in venues:
        bayesian = VenueRating.update_bayesian_for_venue(venue)
        # If bayesian_rating is None (no ratings), treat score as -1 so
        # unrated venues sort to the bottom of recommendations.
        br = bayesian.get('bayesian_rating') if isinstance(bayesian, dict) else None
        score = br if br is not None else -1
        venue_list.append({
            'venue': venue,
            'bayesian_rating': score
        })
    # Sort venues by bayesian_rating descending
    sorted_venues = sorted(venue_list, key=lambda x: x['bayesian_rating'], reverse=True)
    # Return all venues in sorted order (frontend controls how many to show)
    top_venues = [v['venue'] for v in sorted_venues]
    serializer = VenueSerializer(top_venues, many=True)
    return Response(serializer.data)


# Restore FavoriteVenueViewSet
class FavoriteVenueViewSet(viewsets.ModelViewSet):
    queryset = FavoriteVenue.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = FavoriteVenueSerializer

    def perform_create(self, serializer):
        from django.db import IntegrityError
        from rest_framework import serializers
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise serializers.ValidationError({"detail": "You have already favorited this venue."})
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



# VenueViewSet for /api/venues/owner/ to return bookings_count and pending_requests
class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        # If the user is authenticated and is a venue owner, return only their venues with booking stats
        if user.is_authenticated and hasattr(user, 'user_type') and user.user_type == 'venue_owner':
            from django.db.models import Count, Q, Avg
            return (
                Venue.objects.filter(owner=user)
                .annotate(
                    bookings_count=Count('events__reservations', filter=Q(events__reservations__status='approved'), distinct=True),
                    pending_requests=Count('events__reservations', filter=Q(events__reservations__status='pending'), distinct=True),
                    avg_rating=Avg('ratings__rating')
                )
            )
        # Otherwise, return all venues
        return Venue.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        venue_id = self.request.query_params.get('venue')
        if venue_id:
            # Only include events for this venue that have an approved reservation
            queryset = queryset.filter(
                venue_id=venue_id,
                reservations__status='approved'
            ).distinct()
        return queryset

    def perform_create(self, serializer):
            venue_id = self.request.data.get('venue')
            if not venue_id:
                raise serializers.ValidationError({'venue': 'This field is required.'})
            try:
                venue = Venue.objects.get(id=venue_id)
            except Venue.DoesNotExist:
                raise serializers.ValidationError({'venue': 'Venue not found.'})
            serializer.save(organizer=self.request.user, venue=venue)

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

        user = request.user

        # Prevent same user from sending multiple requests for same venue/date/event
        existing_pending = Reservation.objects.filter(
            user=user,
            event__venue=event.venue,
            event__date=event.date,
            status='pending'
        ).exists()
        if existing_pending:
            return Response({'error': 'You have already sent a booking request for this venue and date.'}, status=400)

        # Only block if there is an event for this venue/date with an approved reservation
        same_venue_events = Event.objects.filter(venue=event.venue, date=event.date).exclude(id=event.id)
        for ev in same_venue_events:
            approved = Reservation.objects.filter(event=ev, status='approved').exists()
            if approved:
                return Response({'error': 'This venue is already booked for the selected date.'}, status=400)

        # Create reservation
        reservation = Reservation.objects.create(user=user, event=event, status='pending')
        from .serializers import ReservationSerializer
        serializer = ReservationSerializer(reservation)
        # Notify venue owner by email about the new booking request
        try:
            owner = event.venue.owner
            owner_email = getattr(owner, 'email', None)
            if owner_email:
                subject = f"New Booking Request for {event.venue.name}"
                message = (
                    f"Hi {getattr(owner, 'name', 'Owner')},\n\n"
                    f"{getattr(user, 'name', user.email)} has requested a booking for {event.venue.name} on {event.date.strftime('%Y-%m-%d')}.\n"
                    "Please review and approve or reject the request in your owner dashboard.\n\n"
                    "Regards,\nVenueBook Team"
                )
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [owner_email],
                    fail_silently=False,
                )
                logging.info(f"Booking request email sent to owner {owner_email} for reservation {reservation.id}")
        except Exception:
            logging.exception(f"Failed to send booking request email for reservation {reservation.id}")
        return Response(serializer.data, status=201)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        reservation = self.get_object()
        # Only the owner of the venue can approve
        if reservation.event.venue.owner != request.user:
            return Response({'detail': 'Not allowed.'}, status=403)
        reservation.status = 'approved'
        reservation.save()
        # Send email to user notifying approval
        user = reservation.user
        event = reservation.event
        venue = event.venue
        try:
            send_mail(
                'Your Venue Booking is Approved',
                f"Hi {user.name}, your booking for {venue.name} on {event.date.strftime('%Y-%m-%d')} has been approved!",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            logging.info(f"Approval email sent to {user.email} for reservation {reservation.id}")
        except Exception:
            logging.exception(f"Failed to send approval email for reservation {reservation.id} to {user.email}")
        return Response({'status': 'approved'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        reservation = self.get_object()
        # Only the owner of the venue can reject
        if reservation.event.venue.owner != request.user:
            return Response({'detail': 'Not allowed.'}, status=403)
        reservation.status = 'rejected'
        reservation.save()
        # Send email to user notifying rejection
        user = reservation.user
        event = reservation.event
        venue = event.venue
        try:
            send_mail(
                'Your Venue Booking is Rejected',
                f"Hi {user.name}, your booking for {venue.name} on {event.date.strftime('%Y-%m-%d')} has been rejected.",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            logging.info(f"Rejection email sent to {user.email} for reservation {reservation.id}")
        except Exception:
            logging.exception(f"Failed to send rejection email for reservation {reservation.id} to {user.email}")
        return Response({'status': 'rejected'})






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
        users = CustomUser.objects.all()
        user_data = []
        from .models import Venue, Reservation
        for user in users:
            venues_count = 0
            bookings_count = 0
            if user.user_type == 'venue_owner':
                venues_count = Venue.objects.filter(owner=user).count()
            bookings_count = Reservation.objects.filter(user=user).count()
            user_data.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'user_type': user.user_type,
                'date_joined': user.date_joined,
                'is_active': user.is_active,
                'venues': venues_count,
                'bookings': bookings_count,
            })
        return Response(user_data)

class AdminVenueList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        venues = Venue.objects.all()
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)

class AdminBookingList(APIView):
    permission_classes = [IsAdminUser]


    def get(self, request):
        bookings = Reservation.objects.select_related('event__venue', 'user', 'event').all()
        serializer = AdminBookingSerializer(bookings, many=True)
        return Response(serializer.data)

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
            'phone': user.phone,
            'address': user.address,
            'profile_image': user.profile_image,
        })

    def patch(self, request):
        user = request.user
        data = request.data
        updated = False
        for field in ['name', 'email', 'phone', 'address', 'profile_image']:
            if field in data:
                setattr(user, field, data[field])
                updated = True
        if updated:
            user.save()
        return Response({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'user_type': user.user_type,
            'date_joined': user.date_joined,
            'is_active': user.is_active,
            'phone': user.phone,
            'address': user.address,
            'profile_image': user.profile_image,
        })
