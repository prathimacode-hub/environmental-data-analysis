import pandas as pd
import numpy as np


def create_time_features(df: pd.DataFrame, date_column: str = "date") -> pd.DataFrame:
    """
    Extract time-based features from datetime column.
    """
    if date_column in df.columns:
        df[date_column] = pd.to_datetime(df[date_column], errors="coerce")

        df["year"] = df[date_column].dt.year
        df["month"] = df[date_column].dt.month
        df["day"] = df[date_column].dt.day
        df["dayofweek"] = df[date_column].dt.dayofweek
        df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)

    return df


def create_lag_features(df: pd.DataFrame, target_column: str = "aqi", lags: list = [1, 3, 7]) -> pd.DataFrame:
    """
    Create lag features for time-series modeling.
    """
    for lag in lags:
        df[f"{target_column}_lag_{lag}"] = df[target_column].shift(lag)

    return df


def create_rolling_features(df: pd.DataFrame, target_column: str = "aqi", windows: list = [3, 7, 14]) -> pd.DataFrame:
    """
    Create rolling mean features.
    """
    for window in windows:
        df[f"{target_column}_rolling_mean_{window}"] = (
            df[target_column].rolling(window=window).mean()
        )

    return df


def create_pollutant_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create ratios between pollutants (if available).
    """
    cols = df.columns

    if "pm25" in cols and "pm10" in cols:
        df["pm25_pm10_ratio"] = df["pm25"] / (df["pm10"] + 1e-6)

    if "no2" in cols and "so2" in cols:
        df["no2_so2_ratio"] = df["no2"] / (df["so2"] + 1e-6)

    return df


def encode_categorical(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encode categorical columns using one-hot encoding.
    """
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns

    if len(categorical_cols) > 0:
        df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    return df


def drop_unnecessary_columns(df: pd.DataFrame, columns_to_drop: list = ["date"]) -> pd.DataFrame:
    """
    Drop columns not needed for modeling.
    """
    for col in columns_to_drop:
        if col in df.columns:
            df = df.drop(columns=[col])

    return df


def handle_missing_after_fe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values generated after lag/rolling features.
    """
    return df.dropna()


def feature_engineering_pipeline(df: pd.DataFrame, target_column: str = "aqi") -> pd.DataFrame:
    """
    Full feature engineering pipeline.
    """
    df = create_time_features(df)
    df = create_lag_features(df, target_column)
    df = create_rolling_features(df, target_column)
    df = create_pollutant_ratios(df)
    df = encode_categorical(df)
    df = drop_unnecessary_columns(df)
    df = handle_missing_after_fe(df)

    return df
