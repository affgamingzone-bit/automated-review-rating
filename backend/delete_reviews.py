import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Review

# Delete the last 7 reviews
deleted_count, _ = Review.objects.all().order_by('-created_at')[:7].delete()
print(f"Successfully deleted {deleted_count} reviews from the database.")
