import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Review

# Delete the last (most recent) review
last_review = Review.objects.all().order_by('-created_at').first()
if last_review:
    review_id = last_review.id
    last_review.delete()
    print(f"Successfully deleted review ID {review_id} from the database.")
else:
    print("No reviews found in the database.")
