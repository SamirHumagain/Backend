
from django.db import models
from django.conf import settings

def upload_venue_image(instance, filename):
    return f'venue_images/{instance.owner.username}/{filename}'

class Venue(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    capacity = models.IntegerField()
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_venue_image, null=True, blank=True)
    available = models.BooleanField(default=True)

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, default='pending')



