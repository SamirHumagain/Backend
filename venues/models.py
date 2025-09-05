
from django.db import models
from django.conf import settings


class Venue(models.Model):
    image = models.URLField(max_length=500, default="https://example.com/default-image.jpg")
    status = models.CharField(max_length=50, default="pending")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    location_name = models.CharField(max_length=255, blank=True, default="")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_venues')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events')
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reservations')
    reserved_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")  # pending, approved, rejected

    def __str__(self):
        return f"{self.user.email} - {self.event.name}"

class FavoriteVenue(models.Model):
    added_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_venues')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = ('user', 'venue')

    def __str__(self):
        return f"{self.user.email} - {self.venue.name}"

class VenueRating(models.Model):
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='venue_ratings')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='ratings')

    class Meta:
        unique_together = ('user', 'venue')

    def __str__(self):
        return f"{self.user.email} - {self.venue.name} ({self.rating})"

