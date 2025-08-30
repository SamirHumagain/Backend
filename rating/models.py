

# Create your models here.
from django.db import models
from django.conf import settings
from venues.models import Venue, Reservation

class VenueRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='ratings')
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='rating')
    rating = models.PositiveSmallIntegerField()  # 1–5 stars
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'venue')

    def __str__(self):
        return f"{self.venue.name} - {self.rating} stars by {self.user.username}"
