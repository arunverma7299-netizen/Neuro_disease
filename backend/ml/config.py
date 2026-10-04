from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"
ML_ROOT = BACKEND_ROOT / "ml"

RAW_DATA_PATH = ML_ROOT / "data" / "raw" / "neuropulse_dataset.csv"
PROCESSED_DATA_DIR = ML_ROOT / "data" / "processed"
REPORTS_DIR = ML_ROOT / "reports"
ARTIFACTS_DIR = ML_ROOT / "artifacts"

USER_ID_COLUMN = "User_ID"
TARGET_COLUMN = "Target"
SCORE_COLUMN = "Burnout_Risk_Pct"

TARGET_ORDER = ["Calm", "Balanced", "Strained", "Overloaded"]

TARGET_UI_SCORE_BANDS = {
    "Calm": (0, 30),
    "Balanced": (31, 50),
    "Strained": (51, 70),
    "Overloaded": (71, 100),
}

TARGET_SCORE_CENTERS = {
    "Calm": 15,
    "Balanced": 40,
    "Strained": 60,
    "Overloaded": 85,
}

CORE_MODEL_FEATURES = [
    "Sleep_Hours",
    "Sleep_Quality",
    "Screen_Time_Hours",
    "Work_Study_Hours",
    "Exercise_Minutes",
    "Caffeine_Cups",
    "Water_Liters",
    "Stress_Level",
    "Social_Interaction_Hours",
    "Resting_Heart_Rate",
]

ALL_ANALYSIS_FEATURES = [
    "Age",
    "Gender",
    "Occupation",
    "Day_Type",
    "Sleep_Hours",
    "Sleep_Quality",
    "Screen_Time_Hours",
    "Social_Media_Hours",
    "Work_Study_Hours",
    "Exercise_Minutes",
    "Steps_Per_Day",
    "Caffeine_Cups",
    "Water_Liters",
    "Diet_Quality",
    "Meditation_Minutes",
    "Social_Interaction_Hours",
    "Outdoor_Time_Minutes",
    "Alcohol_Units",
    "Resting_Heart_Rate",
    "HRV_ms",
    "Stress_Level",
    "Anxiety_Score",
    "Mood_Score",
    "Energy_Level",
    "Focus_Score",
    SCORE_COLUMN,
]

FEATURE_NOTES = {
    "User_ID": "Unique row identifier. It helps trace records but is never used as a predictive feature.",
    "Target": "Educational lifestyle-state label used as the classification target.",
    "Age": "Participant age. Useful for analysis, but not part of the first user-facing scan inputs.",
    "Gender": "Self-reported gender. Kept for exploration only.",
    "Occupation": "Occupation category such as Student or Teacher. Helpful for analysis of routine patterns.",
    "Day_Type": "Weekday or Weekend. Helps explain routine differences.",
    "Sleep_Hours": "Hours slept in the last day/night.",
    "Sleep_Quality": "Self-rated sleep quality on the dataset scale.",
    "Screen_Time_Hours": "Total screen exposure in hours.",
    "Social_Media_Hours": "Time spent on social platforms.",
    "Work_Study_Hours": "Time spent working or studying.",
    "Exercise_Minutes": "Physical activity duration in minutes.",
    "Steps_Per_Day": "Daily movement proxy measured as step count.",
    "Caffeine_Cups": "Caffeine intake measured in cups.",
    "Water_Liters": "Estimated water intake in liters.",
    "Diet_Quality": "Self-rated diet quality on the dataset scale.",
    "Meditation_Minutes": "Time spent meditating or doing calm-focus activities.",
    "Social_Interaction_Hours": "Time spent in social interaction.",
    "Outdoor_Time_Minutes": "Minutes spent outdoors.",
    "Alcohol_Units": "Alcohol intake in units.",
    "Resting_Heart_Rate": "Resting heart rate, used as a lifestyle signal rather than a medical conclusion.",
    "HRV_ms": "Heart-rate variability measured in milliseconds.",
    "Stress_Level": "Self-reported stress on the dataset scale.",
    "Anxiety_Score": "Self-reported anxiety score in the dataset. Treated as an analysis-only feature in Phase 1.",
    "Mood_Score": "Self-reported mood score in the dataset. Used only for analysis.",
    "Energy_Level": "Self-reported energy level in the dataset. Used only for analysis.",
    "Focus_Score": "Self-reported focus score in the dataset. Used only for analysis.",
    SCORE_COLUMN: "Educational risk-style score already present in the dataset. Kept as a reference signal, not used as an input feature.",
}

EXPECTED_RANGES = {
    "Age": (0, 120),
    "Sleep_Hours": (0, 24),
    "Sleep_Quality": (1, 10),
    "Screen_Time_Hours": (0, 24),
    "Social_Media_Hours": (0, 24),
    "Work_Study_Hours": (0, 24),
    "Exercise_Minutes": (0, 600),
    "Steps_Per_Day": (0, 50000),
    "Caffeine_Cups": (0, 20),
    "Water_Liters": (0, 10),
    "Diet_Quality": (1, 10),
    "Meditation_Minutes": (0, 600),
    "Social_Interaction_Hours": (0, 24),
    "Outdoor_Time_Minutes": (0, 1440),
    "Alcohol_Units": (0, 50),
    "Resting_Heart_Rate": (30, 200),
    "HRV_ms": (0, 300),
    "Stress_Level": (1, 10),
    "Anxiety_Score": (1, 10),
    "Mood_Score": (1, 10),
    "Energy_Level": (1, 10),
    "Focus_Score": (1, 10),
    SCORE_COLUMN: (0, 100),
}

LEAKAGE_COLUMNS = [SCORE_COLUMN, "Anxiety_Score", "Mood_Score", "Energy_Level", "Focus_Score"]
