# src/__init__.py

"""
Core data processing and machine learning module
for Environmental Data Analysis project.
"""

# Data preprocessing
from .data_preprocessing import preprocess_data

# Feature engineering
from .feature_engineering import feature_engineering_pipeline

# Model utilities
from .model import (
    load_model,
    predict,
    train_model,
    evaluate_model,
)

# Utility helpers
from .utils import (
    load_csv,
    save_csv,
    load_pickle,
    save_pickle,
    categorize_aqi,
    align_features,
)
