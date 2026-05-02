import os
import pandas as pd
import json
import joblib


# ==============================
# FILE & PATH UTILITIES
# ==============================

def ensure_dir(path: str):
    """
    Create directory if it does not exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def get_abs_path(*paths):
    """
    Build absolute path from relative segments.
    """
    return os.path.abspath(os.path.join(*paths))


# ==============================
# DATA UTILITIES
# ==============================

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load CSV file safely.
    """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise Exception(f"Error loading CSV: {e}")


def save_csv(df: pd.DataFrame, file_path: str):
    """
    Save DataFrame to CSV.
    """
    try:
        ensure_dir(os.path.dirname(file_path))
        df.to_csv(file_path, index=False)
    except Exception as e:
        raise Exception(f"Error saving CSV: {e}")


# ==============================
# MODEL UTILITIES
# ==============================

def save_pickle(obj, file_path: str):
    """
    Save object as pickle file.
    """
    try:
        ensure_dir(os.path.dirname(file_path))
        joblib.dump(obj, file_path)
    except Exception as e:
        raise Exception(f"Error saving pickle: {e}")


def load_pickle(file_path: str):
    """
    Load pickle file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    return joblib.load(file_path)


# ==============================
# JSON UTILITIES
# ==============================

def save_json(data: dict, file_path: str):
    """
    Save dictionary as JSON.
    """
    try:
        ensure_dir(os.path.dirname(file_path))
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise Exception(f"Error saving JSON: {e}")


def load_json(file_path: str):
    """
    Load JSON file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r") as f:
        return json.load(f)


# ==============================
# LOGGING / PRINT HELPERS
# ==============================

def log(message: str):
    """
    Simple logger (can be replaced with logging module later).
    """
    print(f"[INFO] {message}")


# ==============================
# AQI UTILITIES (DOMAIN LOGIC)
# ==============================

def categorize_aqi(aqi_value: float) -> str:
    """
    Convert AQI value into category.
    """
    if aqi_value <= 50:
        return "Good"
    elif aqi_value <= 100:
        return "Moderate"
    elif aqi_value <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi_value <= 200:
        return "Unhealthy"
    elif aqi_value <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"


# ==============================
# FEATURE UTILITIES
# ==============================

def align_features(input_df: pd.DataFrame, feature_columns: list) -> pd.DataFrame:
    """
    Ensure input dataframe has same columns as training data.
    """
    for col in feature_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    return input_df[feature_columns]
