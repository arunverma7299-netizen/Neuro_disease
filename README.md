# NeuroPulse

NeuroPulse is a futuristic, educational mental-load and lifestyle insights project. It is designed to feel like an AI health-tech product while staying simple enough to run locally and explain clearly.

Important: this project is not a medical diagnosis system. It only estimates an educational lifestyle-based state such as Calm, Balanced, Strained, or Overloaded.

## Architecture

The project is being built in phases.

1. Phase 1: dataset inspection, feature explanation, data cleaning, and target validation.
2. Phase 2: Decision Tree training and explainability.
3. Phase 3: Random Forest and Extra Trees training.
4. Phase 4: hyperparameter tuning and cross-validation.
5. Phase 5: model export and saved artifacts.
6. Phase 6: FastAPI backend.
7. Phase 7+: React frontend, Three.js brain, animations, history, and what-if simulation.

## Current Phase 1 Scope

The provided dataset already contains a clean educational label column named `Target` and a continuous reference score named `Burnout_Risk_Pct`.

Phase 1 does the following:

1. Inspects the dataset shape, dtypes, and missing values.
2. Explains every feature in plain language.
3. Identifies categorical and numerical columns.
4. Detects obvious data-quality issues.
5. Confirms the existing label structure without fabricating medical labels.
6. Builds a cleaned model frame that keeps only the scan features intended for the user-facing product.

## Dataset Summary

- Rows: 3000
- Columns: 28
- Missing values: none
- Target classes: Calm, Balanced, Strained, Overloaded

The dataset is already suitable for an educational classifier. The score column can be used later for transparent score mapping, but it is not used as a training feature to avoid leakage.

## Core Scan Inputs

The product-level NeuroScan will focus on these user-facing features:

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

## How to Run Phase 1

1. Put the CSV at `backend/ml/data/raw/neuropulse_dataset.csv`.
2. Install the Python dependencies listed in `backend/requirements.txt`.
3. Run `python backend/ml/01_data_preparation.py`.
4. Run `python backend/ml/02_eda.py`.

The scripts will generate cleaned data and a Markdown EDA report under `backend/ml/data/processed` and `backend/ml/reports`.

## Current Project Status

The project now includes:

1. Phase 1 ML preparation and EDA.
2. A FastAPI backend scaffold with SQLite history support.
3. A starter React frontend with the futuristic NeuroPulse UI shell.

The frontend is already connected to the backend prediction endpoint shape and falls back to a local estimate until the trained model artifact is available.

## Running The App

Backend:

1. `cd backend`
2. `python -m uvicorn app.main:app --reload`

Frontend:

1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Notes

- The trained classifier is not saved yet, so `/predict` currently returns a clear unavailable response until Phase 2+ training artifacts are created.
- The UI is a usable starting shell, not the final polished product. The remaining phases will add the trained model, live history, decision-tree explainability, and the richer Three.js interactions.

## Medical / Educational Disclaimer

NeuroPulse is for educational lifestyle insight only. It does not diagnose anxiety, depression, neurological disorders, or any disease.
