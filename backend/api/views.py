from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer, PredictionInputSerializer
import joblib
import os
from django.conf import settings
import re
import numpy as np

# Load the trained model, vectorizer, and SVD from models folder
# Try multiple paths: first in backend/models, then in root models folder
POSSIBLE_PATHS = [
    os.path.join(settings.BASE_DIR, 'models'),  # backend/models
    os.path.join(settings.BASE_DIR.parent, 'models'),  # root/models
]

print(f"[DEBUG] BASE_DIR: {settings.BASE_DIR}")
print(f"[DEBUG] BASE_DIR.parent: {settings.BASE_DIR.parent}")

MODELS_DIR = None
for path in POSSIBLE_PATHS:
    print(f"[DEBUG] Checking path: {path}")
    if os.path.exists(path):
        print(f"[DEBUG] Found models directory at: {path}")
        MODELS_DIR = path
        break

if MODELS_DIR is None:
    MODELS_DIR = os.path.join(settings.BASE_DIR, 'models')
    print(f"[DEBUG] Using default models directory: {MODELS_DIR}")

MODEL_PATH = os.path.join(MODELS_DIR, 'best_ml_model.pkl')
VECTORIZER_PATH = os.path.join(MODELS_DIR, 'best_ml_vectorizer.pkl')
SVD_PATH = os.path.join(MODELS_DIR, 'best_ml_svd.pkl')

print(f"[DEBUG] Looking for models at:")
print(f"[DEBUG]   Model: {MODEL_PATH}")
print(f"[DEBUG]   Vectorizer: {VECTORIZER_PATH}")
print(f"[DEBUG]   SVD: {SVD_PATH}")

model = None
vectorizer = None
svd = None

try:
    print(f"[DEBUG] Attempting to load model from: {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    print("✅ ML model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print(f"[DEBUG] File exists: {os.path.exists(MODEL_PATH)}")
    print(f"[DEBUG] Directory contents: {os.listdir(MODELS_DIR) if os.path.exists(MODELS_DIR) else 'Directory not found'}")
    model = None

try:
    print(f"[DEBUG] Attempting to load vectorizer from: {VECTORIZER_PATH}")
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("✅ Vectorizer loaded successfully!")
except Exception as e:
    print(f"❌ Error loading vectorizer: {e}")
    vectorizer = None

try:
    print(f"[DEBUG] Attempting to load SVD from: {SVD_PATH}")
    svd = joblib.load(SVD_PATH)
    print("✅ SVD loaded successfully!")
except Exception as e:
    print(f"❌ Error loading SVD: {e}")
    svd = None


def clean_text(text):
    """
    Clean the review text (customize based on your training preprocessing)
    This should match the cleaning done during model training
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint - reports if the service and models are ready
    """
    health_status = {
        'status': 'healthy' if (model and vectorizer and svd) else 'degraded',
        'django': 'ok',
        'database': 'ok',
        'models': {
            'model': 'loaded' if model else 'not_loaded',
            'vectorizer': 'loaded' if vectorizer else 'not_loaded',
            'svd': 'loaded' if svd else 'not_loaded'
        }
    }
    
    http_status = status.HTTP_200_OK if health_status['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
    return Response(health_status, status=http_status)


@api_view(['POST'])
def predict_rating(request):
    """
    Predict rating for a given review text using ML model with vectorizer and SVD
    """
    serializer = PredictionInputSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'error': 'Invalid input', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if model is None:
        return Response(
            {'error': 'Model not loaded. Please ensure best_ml_model.pkl exists in the models directory.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if vectorizer is None:
        return Response(
            {'error': 'Vectorizer not loaded. Please ensure best_ml_vectorizer.pkl exists in the models directory.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if svd is None:
        return Response(
            {'error': 'SVD not loaded. Please ensure best_ml_svd.pkl exists in the models directory.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    try:
        # Get the review text
        review_text = serializer.validated_data['review_text']
        
        # Clean the text
        cleaned_text = clean_text(review_text)
        
        # Vectorize the text
        vectorized_text = vectorizer.transform([cleaned_text])
        
        # Apply SVD transformation
        reduced_text = svd.transform(vectorized_text)
        
        # Make prediction with probability scores
        prediction = model.predict(reduced_text)[0]
        probabilities = model.predict_proba(reduced_text)[0]
        
        # Get the class with highest probability
        predicted_class = model.classes_[probabilities.argmax()]
        confidence = float(np.max(probabilities))
        
        # Save to database
        review = Review.objects.create(
            cleaned_text=cleaned_text,
            predicted_score=int(predicted_class)
        )
        
        # Serialize and return
        response_serializer = ReviewSerializer(review)
        
        return Response(
            {
                'success': True,
                'data': response_serializer.data,
                'confidence': confidence,
                'message': 'Prediction completed successfully'
            },
            status=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        return Response(
            {'error': 'Prediction failed', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_all_reviews(request):
    """
    Get all reviews
    """
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(
        {
            'success': True,
            'data': serializer.data,
            'count': reviews.count()
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_review(request, pk):
    """
    Get a specific review by ID
    """
    try:
        review = Review.objects.get(pk=pk)
        serializer = ReviewSerializer(review)
        return Response(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    except Review.DoesNotExist:
        return Response(
            {'error': 'Review not found'},
            status=status.HTTP_404_NOT_FOUND
        )
