# NeuroPulse Synopsis

## Project Title
**NeuroPulse**

## Tagline
**Understand your mind. One day at a time.**

## Project Overview
NeuroPulse is an educational AI-powered lifestyle insights application that estimates a user's mental-load state from daily habits such as sleep, screen time, exercise, stress, hydration, and social activity. The application is designed to look and feel like a futuristic health-tech product while remaining simple enough to run locally.

The project is not a medical diagnosis system. It does not diagnose anxiety, depression, neurological disorders, or any disease. Instead, it classifies users into one of four educational states:

- Calm
- Balanced
- Strained
- Overloaded

## Problem Statement
Most lifestyle dashboards are either too basic or too clinical. NeuroPulse solves this by combining:

- Clear machine learning
- Explainable predictions
- A premium 3D experience
- A conversational scan flow
- A backend API
- A modern React frontend

## Dataset Used
The project uses a lifestyle and wellness dataset with:

- 3,000 rows
- 28 columns
- No missing values
- No duplicate rows

Important features include:

- Sleep duration
- Sleep quality
- Screen time
- Work or study hours
- Exercise duration
- Caffeine intake
- Water intake
- Self-reported stress
- Social activity
- Resting heart rate

The existing Target column was used as the educational class label. Leakage-prone columns such as Burnout_Risk_Pct and other self-report outcome scores were excluded from training.

## Machine Learning Approach
NeuroPulse keeps the ML stack intentionally understandable.

### Models Trained
- Decision Tree Classifier
- Random Forest Classifier
- Extra Trees Classifier

### Validation Strategy
- Train/test split
- Stratified cross-validation
- GridSearchCV
- RandomizedSearchCV

### Best Model
The best model selected for the final artifact is Random Forest.

### Final Test Performance
- Accuracy: 0.8750
- Precision (macro): 0.8779
- Recall (macro): 0.8737
- F1-score (macro): 0.8757

## Backend
The backend uses FastAPI and SQLite.

### API Endpoints
- GET /health
- POST /predict
- POST /simulate
- GET /history
- POST /history
- GET /model-info
- POST /feedback

The backend returns:
- Predicted class
- Score
- Confidence
- Top factors
- Simplified decision path

## Frontend
The frontend uses React, TypeScript, Three.js, React Three Fiber, Framer Motion, Recharts, and Lucide React.

### Main UI Features
- Futuristic landing page
- Rotating 3D brain
- Step-by-step NeuroScan questions
- Animated result screen
- Decision-path explanation section
- What-If simulator
- Neuro Journey chart
- Inside the AI page
- Daily Neuro Mission interaction

## Explainability
A Decision Tree model is also trained so the project can present human-readable reasoning. The explanations are framed as learned thresholds and lifestyle patterns, not medical causes.

## Why This Project Is Good for a College Submission
NeuroPulse demonstrates:

- Dataset inspection
- Data cleaning
- Feature selection
- Classification
- Ensemble learning
- Hyperparameter tuning
- Cross-validation
- Model comparison
- API integration
- Frontend/backend integration
- Product-level UI/UX design

## How to Run
### Backend
1. `cd backend`
2. `python -m uvicorn app.main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Final Note
NeuroPulse is an educational project only. It should be presented as a lifestyle and mental-load insights tool, not as a medical diagnostic system.
