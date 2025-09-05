from django.db import models
from django.conf import settings
from venues.models import Venue

class VenueRating(models.Model):
    # Bayesian rating fields for the venue
    num_ratings = models.PositiveIntegerField(default=0)
    sum_ratings = models.PositiveIntegerField(default=0)
    bayesian_rating = models.FloatField(default=0.0)

    @staticmethod
    def update_bayesian_for_venue(venue, min_num=5, global_avg=None):
        """
        Calculate Bayesian average rating for the venue.
        min_num: minimum ratings to balance (prior strength)
        global_avg: average rating across all venues
        """
        from django.db.models import Avg, Sum
        n = venue.ratings.count()
        s = venue.ratings.aggregate(total=Sum('rating'))['total'] or 0
        # Use a sensible default for global_avg if no ratings exist
        if global_avg is None:
            global_avg = VenueRating.objects.aggregate(avg=Avg('rating'))['avg']
            if global_avg is None or global_avg == 0:
                global_avg = 3.0  # fallback to neutral value if no ratings
        # If no ratings for this venue, use global_avg
        if n == 0:
            bayesian = global_avg
        else:
            bayesian = ((min_num * global_avg) + s) / (min_num + n)
        return {
            'num_ratings': n,
            'sum_ratings': s,
            'bayesian_rating': bayesian
        }
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
