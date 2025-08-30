
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import VenueRating
from django.db.models import Avg

@receiver([post_save, post_delete], sender=VenueRating)
def update_venue_average_rating(sender, instance, **kwargs):
    venue = instance.venue
    avg = venue.ratings.aggregate(Avg('rating'))['rating__avg']
    venue.average_rating = round(avg, 2) if avg else 0.0
    venue.save()
