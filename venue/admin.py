

# Register your models here.
from django.contrib import admin
from .models import Venue, Booking

admin.site.register(Venue)
admin.site.register(Booking)
