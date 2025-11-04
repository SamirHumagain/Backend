from django.core.management.base import BaseCommand
from venues.models import Venue
from eventplanner.models import VenueImage


class Command(BaseCommand):
    help = "Sync each Venue.image to the latest VenueImage entry (useful one-time fix)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--domain",
            type=str,
            default="http://127.0.0.1:8000",
            help="Base domain to build absolute image URLs (default: http://127.0.0.1:8000)",
        )

    def handle(self, *args, **options):
        domain = options.get("domain", "http://127.0.0.1:8000").rstrip("/")
        updated = 0
        for venue in Venue.objects.all():
            latest = VenueImage.objects.filter(venue_id=venue.id).order_by("-id").first()
            if not latest or not getattr(latest, "image", None):
                continue
            try:
                rel = latest.image.url if hasattr(latest.image, "url") else str(latest.image)
                image_url = f"{domain}{rel}"
            except Exception:
                continue
            if venue.image != image_url:
                venue.image = image_url
                venue.save(update_fields=["image"])
                updated += 1
                self.stdout.write(f"Updated venue {venue.id} -> {image_url}")

        self.stdout.write(self.style.SUCCESS(f"Sync complete. Venues updated: {updated}"))
