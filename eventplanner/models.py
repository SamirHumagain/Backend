from django.db import models
from django.conf import settings

class EventType(models.Model):
	name = models.CharField(max_length=100, unique=True)
	label = models.CharField(max_length=100)
	price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	venue = models.ForeignKey('venues.Venue', on_delete=models.CASCADE, related_name='event_types')

	def __str__(self):
		return self.label

# CateringItem as a top-level model
class CateringItem(models.Model):
	SNACK = 'snack'
	MAIN_COURSE = 'main_course'
	TYPE_CHOICES = [
		(SNACK, 'Snack'),
		(MAIN_COURSE, 'Main Course'),
	]
	name = models.CharField(max_length=100)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	type = models.CharField(max_length=20, choices=TYPE_CHOICES)
	venue = models.ForeignKey('venues.Venue', related_name='catering_items', on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.name} ({self.get_type_display()})"

class Service(models.Model):
	venue = models.ForeignKey('venues.Venue', on_delete=models.CASCADE, related_name='services', null=True, blank=True)
	name = models.CharField(max_length=255)
	price = models.DecimalField(max_digits=10, decimal_places=2)

# VenueImage model for multiple images per venue
class VenueImage(models.Model):
	venue = models.ForeignKey('venues.Venue', on_delete=models.CASCADE, related_name='images')
	image = models.URLField(max_length=500)
