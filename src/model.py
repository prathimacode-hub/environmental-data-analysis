import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def split_data(df: pd.DataFrame, target_column: str = "aqi", test_size: float = 0.2):
    """
    Split dataset into train and test sets.
    """
    X = df.drop(columns=[target_column])
    y = df[target_column]

    return train_test_split(X, y, test_size=test_size, random_state=42)


def train_model(X_train, y_train):
    """
    Train ML model.
    """
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance.
    """
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    metrics = {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }

    return metrics


def save_model(model, model_path: str):
    """
    Save trained model to disk.
    """
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)


def load_model(model_path: str):
    """
    Load trained model from disk.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")

    return joblib.load(model_path)


def prepare_input_data(input_dict: dict, feature_columns: list):
    """
    Convert user input into model-ready DataFrame.
    """
    df = pd.DataFrame([input_dict])

    # Ensure all required columns exist
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    # Maintain column order
    df = df[feature_columns]

    return df


def predict(model, input_df: pd.DataFrame):
    """
    Make prediction using trained model.
    """
    prediction = model.predict(input_df)
    return prediction[0]


def full_training_pipeline(df: pd.DataFrame, model_path: str, target_column: str = "aqi"):
    """
    End-to-end training pipeline.
    """
    X_train, X_test, y_train, y_test = split_data(df, target_column)

    model = train_model(X_train, y_train)

    metrics = evaluate_model(model, X_test, y_test)

    save_model(model, model_path)

    return model, metrics, list(X_train.columns)
