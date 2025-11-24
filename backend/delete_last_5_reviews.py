import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Review

# Delete the last 5 reviews (most recent)
last_5_reviews = Review.objects.all().order_by('-created_at')[:3]
deleted_ids = [review.id for review in last_5_reviews]

if deleted_ids:
    deleted_count, _ = Review.objects.filter(id__in=deleted_ids).delete()
    print(f"Successfully deleted {deleted_count} reviews from the database.")
    print(f"Deleted review IDs: {deleted_ids}")
else:
    print("No reviews found in the database.")
