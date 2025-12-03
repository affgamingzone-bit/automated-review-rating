# Render.com Deployment Guide

## Backend Deployment on Render

### Prerequisites
- GitHub account with your code pushed
- Render.com account (free tier available)

### Step 1: Connect GitHub to Render
1. Go to https://dashboard.render.com
2. Click "New Web Service"
3. Select "Build and deploy from a Git repository"
4. Connect your GitHub repo (affgamingzone-bit/automated-review-rating)
5. Grant Render access to your repositories

### Step 2: Configure the Web Service
- **Name:** `automated-review-rating-api`
- **Environment:** Python
- **Region:** Oregon (or closest to you)
- **Branch:** main
- **Build Command:** 
  ```bash
  cd backend && pip install -r requirements.txt && python manage.py collectstatic --noinput
  ```
- **Start Command:** 
  ```bash
  cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:8000
  ```

### Step 3: Add Environment Variables
In Render Dashboard → Environment:
```
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=your-service-name.onrender.com,localhost
CORS_ALLOWED_ORIGINS=https://automated-deployed.vercel.app
```

### Step 4: Add PostgreSQL Database
1. Click "New PostgreSQL"
2. Name: `automated-review-rating-db`
3. Region: Same as web service
4. Render will auto-populate `DATABASE_URL`

### Step 5: Deploy
- Click "Deploy" and wait for build to complete
- Copy your service URL (e.g., `https://automated-review-rating-api.onrender.com`)
- Run migrations:
  ```bash
  # In Render dashboard, go to "Shell" and run:
  python backend/manage.py migrate
  ```

### Step 6: Update Frontend
1. Go to Vercel → Settings → Environment Variables
2. Add/Update:
   ```
   REACT_APP_API_URL=https://automated-review-rating-api.onrender.com/api
   ```
3. Redeploy on Vercel

---

## Using render.yaml (Optional - Advanced)
If you want to use the render.yaml file:
1. Push render.yaml to GitHub
2. In Render dashboard, go to "Blueprints"
3. Select your repository
4. Render will auto-configure from render.yaml

## Important Notes
- **Free tier:** Services spin down after 15 minutes of inactivity
- **Database:** Free PostgreSQL has 90 days retention
- To keep services running, upgrade to paid plan
- Model files are included in the repo, so they'll be deployed

## Monitoring
- Check logs in Render dashboard
- Service URL: https://automated-review-rating-api.onrender.com
- API endpoint: https://automated-review-rating-api.onrender.com/api/predict/
