# NeuroPulse Project Report

## Title
**NeuroPulse**

**Tagline:** Understand your mind. One day at a time.

## Abstract
NeuroPulse is an educational, AI-powered lifestyle insights application that estimates a user's current mental-load state from daily habits such as sleep, screen time, stress, exercise, hydration, and social activity. The project is designed to feel like a futuristic health-tech product while keeping the machine learning stack simple, explainable, and locally runnable.

This project does not diagnose anxiety, depression, neurological disorders, or any disease. It predicts one of four educational classes: Calm, Balanced, Strained, or Overloaded.

## 1. Problem Statement
Many lifestyle and productivity tools either feel too clinical or too generic. NeuroPulse solves this by combining:

- A clean educational ML classifier
- A premium 3D user experience
- Explainable decisions
- A local FastAPI backend
- A React frontend with motion and visual feedback

The goal is to show how data science and product design can work together in one portfolio-grade application.

## 2. Why NeuroPulse?
NeuroPulse was built to demonstrate a complete end-to-end ML product, not just a notebook. It includes:

- Dataset inspection and feature understanding
- Data cleaning and leakage prevention
- Classification with Decision Tree, Random Forest, and Extra Trees
- Hyperparameter tuning and model comparison
- A FastAPI prediction layer
- A futuristic UI with a scan-style flow
- A What-If simulator
- A personal history experience
- An explainability-focused decision tree view

## 3. Dataset Overview
The project uses a lifestyle and wellness dataset with 3,000 rows and 28 columns.

### Dataset Summary
- Rows: 3000
- Columns: 28
- Missing values: 0
- Duplicate rows: 0
- Target classes: Calm, Balanced, Strained, Overloaded

### Categorical Features
- Gender
- Occupation
- Day_Type

### Numerical Features
- Age
- Sleep_Hours
- Sleep_Quality
- Screen_Time_Hours
- Social_Media_Hours
- Work_Study_Hours
- Exercise_Minutes
- Steps_Per_Day
- Caffeine_Cups
- Water_Liters
- Diet_Quality
- Meditation_Minutes
- Social_Interaction_Hours
- Outdoor_Time_Minutes
- Alcohol_Units
- Resting_Heart_Rate
- HRV_ms
- Stress_Level
- Anxiety_Score
- Mood_Score
- Energy_Level
- Focus_Score
- Burnout_Risk_Pct

### Target Interpretation
The dataset already contains an educational label column named Target. The class bands are used as product states, not as medical thresholds:

- Calm: 0–30
- Balanced: 31–50
- Strained: 51–70
- Overloaded: 71–100

The continuous Burnout_Risk_Pct column was treated as a reference signal and excluded from training to avoid leakage.

## 4. Feature Descriptions
The core scan inputs used by the model are:

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

These are lifestyle signals only. They are not used to infer medical conditions.

## 5. Data Preparation
Phase 1 of the project performed the following steps:

1. Inspected the dataset structure, dtypes, and missing values.
2. Identified categorical and numerical columns.
3. Confirmed that there were no missing values.
4. Checked for duplicate rows.
5. Reviewed value ranges for obvious quality issues.
6. Excluded leakage-prone columns from training.
7. Created a cleaned model frame containing only the 10 core scan inputs plus the target label.

### Leakage Prevention
The following columns were not used as input features:
- Burnout_Risk_Pct
- Anxiety_Score
- Mood_Score
- Energy_Level
- Focus_Score

These columns were kept for analysis and transparency, but not for model training.

## 6. Machine Learning Pipeline
The ML pipeline was intentionally kept understandable:

Raw Dataset -> Data Cleaning -> Feature Selection -> Train/Test Split -> Preprocessing Pipeline -> Decision Tree -> Random Forest -> Extra Trees -> Cross Validation -> Hyperparameter Optimization -> Model Comparison -> Best Model -> Save Model

### Modeling Approach
- Decision Tree for explainability
- Random Forest for strong balanced performance
- Extra Trees for another ensemble baseline
- Stratified split to preserve class balance
- Macro F1 used as the key selection metric

### Why Macro F1?
Macro F1 treats all classes more fairly, which matters because the classes are not perfectly balanced.

## 7. Model Comparison
The trained models were compared using the test split.

| Model | Accuracy | Precision (Macro) | Recall (Macro) | F1 (Macro) |
|---|---:|---:|---:|---:|
| Random Forest | 0.8750 | 0.8779 | 0.8737 | 0.8757 |
| Extra Trees | 0.8717 | 0.8725 | 0.8744 | 0.8731 |
| Decision Tree | 0.8533 | 0.8532 | 0.8524 | 0.8525 |

### Best Model
The selected best model is Random Forest.

Reason:
- Highest macro F1
- Strong accuracy
- Good generalization
- Better stability than a single decision tree

## 8. Decision Tree Explainability
Decision Trees are important in NeuroPulse because they provide a readable decision path. The Decision Tree baseline was also trained and exported so the project can show why a prediction happened in a human-readable way.

Example explainable logic:

- Sleep duration is below the learned threshold
- Screen time is relatively high
- Stress level is elevated

This is used as an educational explanation, not a medical conclusion.

## 9. Hyperparameter Tuning
Hyperparameter optimization was performed using:

- GridSearchCV for the Decision Tree
- RandomizedSearchCV for Random Forest and Extra Trees
- StratifiedKFold cross-validation

Parameters tuned included:
- max_depth
- min_samples_split
- min_samples_leaf
- criterion
- n_estimators
- max_features

## 10. Backend Architecture
The backend is built with FastAPI and SQLite.

### Main Endpoints
- GET /health
- POST /predict
- POST /simulate
- GET /history
- POST /history
- GET /model-info
- POST /feedback

### Backend Responsibilities
- Validate input with Pydantic
- Load the trained model artifact
- Return score, state, confidence, top factors, and decision path
- Store history in SQLite
- Expose model metadata for the UI

## 11. Frontend Architecture
The frontend is built with React, TypeScript, Three.js, React Three Fiber, Framer Motion, Tailwind-style custom CSS, Recharts, and Lucide React.

### Core UI Features
- Futuristic landing page
- 3D brain centerpiece
- One-question-at-a-time NeuroScan flow
- Animated result screen
- Why this result? decision-path section
- What-If simulator
- Neuro Journey history page
- Inside the AI page
- Daily Neuro Mission interaction

### Product Design Direction
- Dark futuristic interface
- Glass-like panels
- Subtle neon accents
- Smooth transitions
- Clean typography
- Mobile-friendly layout

## 12. Three.js Brain
The brain is implemented as a stylized procedural 3D object rather than a copyrighted external asset.

It includes:
- Slow rotation
- Soft glow
- Floating particles
- Subtle orbiting animation
- State-based visual intensity

The visual emphasis changes according to the predicted score band.

## 13. Explainability and User Trust
NeuroPulse was designed to explain itself clearly. The app returns:

- Predicted class
- Score
- Confidence
- Top contributing features
- Simplified decision path

The language intentionally uses educational wording such as:

- contributed to this model prediction
- learned threshold
- lifestyle pattern

It does not claim to diagnose or cause any medical state.

## 14. Performance and Accessibility
The project includes:

- Reduced-motion friendly animation patterns
- Keyboard-focusable buttons
- Semantic UI structure
- Accessible labels for inputs
- A responsive layout for desktop and mobile
- A lightweight backend that can run locally

## 15. Results
The current trained model artifact uses the Random Forest classifier as the best model.

### Example Prediction
A smoke test with realistic input values returned:
- Score: 60
- State: Strained
- Confidence: 0.8507

This confirms the backend is connected to the trained ML artifact.

## 16. How to Run the Project
### Backend
1. `cd backend`
2. `python -m uvicorn app.main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## 17. Screenshots
Add project screenshots here after capturing the final UI.

Suggested screenshots:
- Landing page
- NeuroScan question flow
- Result page
- What-If simulator
- Neuro Journey chart
- Inside the AI page

## 18. Future Improvements
Possible future upgrades include:

- Save more scan history entries
- Improve the decision-path generator
- Add more polished mission logic
- Add downloadable reports
- Add PDF export
- Add richer animated transitions
- Add a model comparison dashboard in the UI

## 19. Medical Disclaimer
NeuroPulse is for educational and lifestyle insight only.

It does not diagnose, treat, or replace professional medical advice for anxiety, depression, neurological disorders, or any disease.

## 20. Conclusion
NeuroPulse demonstrates how machine learning, explainability, backend APIs, and modern frontend design can be combined into a polished, portfolio-ready product. The project shows not only classification and model selection, but also the product thinking needed to turn ML into a compelling user experience.
