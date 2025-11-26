# Review Rating Predictor - Full Stack Application

A production-ready full-stack web application that uses machine learning to predict review ratings (1-5 stars) from text. Built with React frontend, Django REST Framework backend, and trained ML models.

## 🌟 Features

- **🤖 AI-Powered Predictions**: Advanced ML models (Random Forest, Logistic Regression, Naive Bayes)
- **⚡ Real-time Processing**: Instant predictions with TF-IDF vectorization and dimensionality reduction
- **📊 Review History**: Complete prediction history with ratings and timestamps
- **🎨 Modern UI**: Responsive React interface with color-coded ratings and visual feedback
- **🔌 REST API**: Full-featured API for predictions and data management
- **📈 Model Performance**: 64.93% test accuracy with Random Forest (best model)
- **🔐 Secure**: Environment-based configuration and proper secret management

## 📋 Prerequisites

- Python 3.8+ (tested with 3.9+)
- Node.js 14+ (tested with 18+)
- npm or yarn
- Git
- Virtual environment support

## 🏗️ Project Structure

```
review-rating-app/
├── backend/                          # Django REST API
│   ├── api/                         # Main API application
│   │   ├── models.py               # Review model
│   │   ├── serializers.py          # Serializers
│   │   ├── views.py                # API endpoints
│   │   ├── urls.py                 # URL routing
│   │   └── migrations/             # Database migrations
│   ├── config/                      # Django configuration
│   │   ├── settings.py             # Settings
│   │   ├── urls.py                 # Root URLs
│   │   └── wsgi.py                 # WSGI config
│   ├── manage.py                   # Django CLI
│   ├── requirements.txt            # Python dependencies
│   ├── db.sqlite3                  # Local database
│   └── retrain_model.py            # Model retraining script
│
├── frontend/                        # React application
│   ├── src/
│   │   ├── components/
│   │   │   ├── ReviewPredictor.js  # Main prediction component
│   │   │   ├── ReviewPredictor.css # Styles
│   │   │   ├── CustomerReviews.js  # Reviews list component
│   │   │   └── CustomerReviews.css # Styles
│   │   ├── App.js                  # Main app component
│   │   ├── App.css                 # App styles
│   │   ├── index.js                # Entry point
│   │   └── index.css               # Global styles
│   ├── public/
│   │   └── index.html              # HTML template
│   ├── package.json                # NPM dependencies
│   └── package-lock.json
│
├── models/                          # ML Models (persistent storage)
│   ├── best_ml_model.pkl           # Random Forest classifier (best)
│   ├── best_ml_vectorizer.pkl      # TF-IDF vectorizer (15k features)
│   └── best_ml_svd.pkl             # SVD transformer (200 components)
│
├── data/                            # Datasets
│   ├── cleaned_dataset/
│   │   └── cleaned_data.csv        # Preprocessed reviews
│   └── extended_dataset/
│       └── Reviews.csv             # Full dataset
│
├── notebooks/                       # Jupyter notebooks
│   ├── cleaned.ipynb              # ML model training & analysis
│   └── extended.ipynb             # Data exploration
│
├── .gitignore                       # Git ignore rules (comprehensive)
├── README.md                        # This file
└── LOGISTIC_REGRESSION_MODEL_REPORT.md  # Model documentation
```

## 🔧 Installation & Setup

### Prerequisites Setup

```bash
# Clone repository
git clone https://github.com/SeionixAi/B116-ADWADH-G--Full-Stack-Automated-Review-Rating-System-.git
cd review-rating-app
```

### Backend Setup

1. **Navigate to backend**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify ML models are in place**
   ```bash
   # Check that models exist in ../models/ folder
   ls ../models/  # or dir ../models/ on Windows
   # Should show: best_ml_model.pkl, best_ml_vectorizer.pkl, best_ml_svd.pkl
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start backend server**
   ```bash
   python manage.py runserver
   ```
   ✅ Backend running on: `http://localhost:8000`

### Frontend Setup

1. **In a new terminal, navigate to frontend**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```
   ✅ Frontend running on: `http://localhost:3000`

## 🎯 Usage

1. **Open browser**: Navigate to `http://localhost:3000`
2. **Enter review**: Type or paste a product review
3. **Click "Predict Rating"**: Get instant ML prediction
4. **View results**:
   - Predicted rating (1-5 stars)
   - Visual representation
   - Confidence score
   - Processed text
5. **View history**: Click "Show Review History" for all predictions

### Example Reviews to Test

```
Positive: "This product is absolutely amazing! Best purchase ever!"
Neutral: "It's okay, nothing special."
Negative: "Terrible quality, broke after one day."
Mixed: "Good value but average quality."
```

## 🔌 API Endpoints

**Base URL**: `http://localhost:8000/api/`

### 1. Predict Review Rating
```http
POST /predict/
Content-Type: application/json

{
  "review_text": "This product is amazing!"
}
```

**Response (201 Created)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "cleaned_text": "product amazing",
    "predicted_score": 5,
    "created_at": "2025-11-26T10:30:00Z"
  },
  "confidence": 0.87,
  "message": "Prediction completed successfully"
}
```

### 2. Get All Reviews
```http
GET /reviews/
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "cleaned_text": "product amazing",
      "predicted_score": 5,
      "created_at": "2025-11-26T10:30:00Z"
    }
  ],
  "count": 1
}
```

### 3. Get Single Review
```http
GET /reviews/{id}/
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "cleaned_text": "product amazing",
    "predicted_score": 5,
    "created_at": "2025-11-26T10:30:00Z"
  }
}
```

## 🧪 Testing with cURL

```bash
# Test prediction
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d "{\"review_text\": \"This product is amazing!\"}"

# Get all reviews
curl http://localhost:8000/api/reviews/

# Get specific review
curl http://localhost:8000/api/reviews/1/
```

## 🤖 Machine Learning Models

### Model Overview

| Model | Test Accuracy | F1-Weighted | Training Time | Status |
|-------|---------------|-------------|---------------|--------|
| **Random Forest** | **0.6493** | **0.6441** | 1201s | ✅ **BEST** |
| Logistic Regression | 0.6239 | 0.6274 | 193s | ✅ Good |
| Naive Bayes | 0.5767 | 0.5788 | 1289s | ✅ Baseline |

### Best Model: Random Forest

**Location**: `models/best_ml_model.pkl`

**Architecture**:
- **Algorithm**: Random Forest Classifier
- **N-Estimators**: 100 decision trees
- **Max Depth**: 20
- **Max Features**: sqrt
- **Class Weight**: Balanced
- **Features**: 200 (after SVD reduction)

**Feature Pipeline**:
1. TF-IDF Vectorization (15,000 features)
   - N-gram range: (1, 2)
   - Min DF: 3, Max DF: 0.9
2. SVD Dimensionality Reduction (200 components)
3. SMOTE Class Balancing

**Performance**:
- Test Accuracy: 64.93%
- F1-Weighted: 0.6441
- F1-Macro: 0.6143
- Cross-Validation Accuracy: 74.73% ± 0.23%

### Text Preprocessing

```python
1. Lowercase conversion
2. NLTK tokenization
3. Stopword removal
4. Lemmatization (WordNetLemmatizer)
5. Token filtering (length > 2)
```

## 📊 Model Training (Optional)

To retrain models with new data:

```bash
cd backend
python retrain_model.py
```

The script will:
1. Load all reviews from database
2. Preprocess text
3. Train Random Forest model
4. Save updated model and vectorizer to `models/` folder

## ⚙️ Configuration

### Backend Settings

Edit `backend/config/settings.py`:

```python
# CORS Origins
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Add production URLs here
]

# Database (default: SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Debug mode (set False in production)
DEBUG = True
```

### Frontend API Configuration

Edit `frontend/src/components/ReviewPredictor.js`:

```javascript
const API_URL = 'http://localhost:8000/api';
```

## 🐛 Troubleshooting

### Backend Issues

**Port 8000 already in use**:
```bash
python manage.py runserver 8001
```

**Model files not found**:
```
Error: Model not loaded. Please ensure best_ml_model.pkl exists in the models directory.
```
Solution: Ensure all three model files are in `models/` folder:
- `best_ml_model.pkl`
- `best_ml_vectorizer.pkl`
- `best_ml_svd.pkl`

**Database migrations fail**:
```bash
python manage.py migrate --run-syncdb
```

### Frontend Issues

**Module not found**:
```bash
rm -rf node_modules package-lock.json
npm install
```

**Port 3000 already in use**:
```bash
PORT=3001 npm start
```

**API connection error**:
- Verify backend is running: `http://localhost:8000`
- Check CORS configuration in `settings.py`
- Verify API_URL in ReviewPredictor.js

### CORS Issues

If you see CORS errors, ensure `django-cors-headers` is installed:
```bash
pip install django-cors-headers
```

## 📱 Admin Panel

Access Django admin: `http://localhost:8000/admin`

**Default URL**: `/admin/`

**Features**:
- View all reviews and predictions
- Filter by rating and date
- Search functionality
- Manage predictions

## 🚀 Production Deployment

### Backend Deployment

1. **Set production settings**:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   SECRET_KEY = 'your-secure-secret-key'  # Use environment variable
   ```

2. **Use production server**:
   ```bash
   gunicorn config.wsgi:application --workers 4
   ```

3. **Set up database**: PostgreSQL recommended
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'review_db',
           'USER': 'postgres',
           'PASSWORD': 'password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

4. **Configure static files**:
   ```bash
   python manage.py collectstatic
   ```

### Frontend Deployment

1. **Build for production**:
   ```bash
   npm run build
   ```

2. **Deploy to Vercel, Netlify, or GitHub Pages**:
   ```bash
   npm install -g netlify-cli
   netlify deploy --prod --dir=build
   ```

## 📚 Documentation

- **[Logistic Regression Model Report](./LOGISTIC_REGRESSION_MODEL_REPORT.md)** - Detailed model analysis
- **[Random Forest Specification](./RANDOM_FOREST_SPECIFICATION.md)** - Best model documentation

## 🔐 Security

- ✅ Environment variables for sensitive data (.env)
- ✅ CORS properly configured
- ✅ No hardcoded secrets in codebase
- ✅ Comprehensive .gitignore (secrets, models, databases)
- ✅ Input validation on API endpoints

## 📦 Dependencies

### Backend
```
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
scikit-learn==1.3.2
pandas==2.1.3
numpy==1.24.3
joblib==1.3.2
tensorflow==2.13.0
```

### Frontend
```
react==19.2.0
react-dom==19.2.0
axios==1.13.2
react-scripts==5.0.1
```

## 📝 License

MIT License - feel free to use for personal and commercial projects.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a Pull Request

## 🎓 Learning Resources

- [Django REST Framework](https://www.django-rest-framework.org/)
- [React Documentation](https://react.dev/)
- [scikit-learn ML Guide](https://scikit-learn.org/)
- [TensorFlow Documentation](https://www.tensorflow.org/)

## 📞 Support

For issues or questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review existing GitHub issues
3. Create a new issue with detailed information

## 🙏 Acknowledgments

- **Django & Django REST Framework** - Backend framework
- **React** - Frontend library
- **scikit-learn** - Machine learning algorithms
- **pandas & numpy** - Data processing
- **TensorFlow** - Deep learning capabilities

---

**Last Updated**: November 26, 2025  
**Version**: 1.0.0  
**Status**: Production Ready ✅

**Happy Predicting! 🎯**
