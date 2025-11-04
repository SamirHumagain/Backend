from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
import os


class Command(BaseCommand):
    help = 'Repair user profile_image fields that contain bare filenames by resolving them to MEDIA URLs'

    def add_arguments(self, parser):
        parser.add_argument('--site', dest='site_url', help='Base site URL to prefix MEDIA paths (e.g. http://localhost:8000)')

    def handle(self, *args, **options):
        site = options.get('site_url') or os.getenv('SITE_URL') or 'http://localhost:8000'
        from loginsignup.models import CustomUser

        users = CustomUser.objects.all()
        updated = 0
        not_found = []

        for user in users:
            val = user.profile_image
            if not val:
                continue
            # skip already absolute URLs or data URLs
            if isinstance(val, str) and (val.startswith('http://') or val.startswith('https://') or val.startswith('data:') or val.startswith('/')):
                continue

            # At this point we assume it's a bare filename; check common locations under MEDIA_ROOT
            candidates = [
                os.path.join(settings.MEDIA_ROOT, 'profile_images', val),
                os.path.join(settings.MEDIA_ROOT, val),
            ]
            found = None
            for c in candidates:
                if os.path.exists(c):
                    found = c
                    break

            if not found:
                not_found.append((user.id, val))
                continue

            # Build relative path and absolute URL
            rel = os.path.relpath(found, settings.MEDIA_ROOT).replace('\\', '/')
            new_url = site.rstrip('/') + settings.MEDIA_URL + rel

            # Save updated URL
            user.profile_image = new_url
            try:
                with transaction.atomic():
                    user.save(update_fields=['profile_image'])
                    updated += 1
            except Exception as e:
                self.stderr.write(f'Failed to update user {user.id}: {e}')

        self.stdout.write(self.style.SUCCESS(f'Updated {updated} users'))
        if not_found:
            self.stdout.write('Files not found for the following users (id, filename):')
            for u in not_found:
                self.stdout.write(f' - {u[0]}: {u[1]}')