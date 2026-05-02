import pandas as pd
import numpy as np


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load dataset from CSV file.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise Exception(f"Error loading data: {e}")


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names (lowercase, replace spaces with underscore).
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w\s]", "", regex=True)
    )
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values:
    - Numerical → fill with median
    - Categorical → fill with mode
    """
    for col in df.columns:
        if df[col].dtype in ["float64", "int64"]:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mode()[0])

    return df


def convert_datetime(df: pd.DataFrame, date_column: str = "date") -> pd.DataFrame:
    """
    Convert date column to datetime and extract features.
    """
    if date_column in df.columns:
        df[date_column] = pd.to_datetime(df[date_column], errors="coerce")

        df["year"] = df[date_column].dt.year
        df["month"] = df[date_column].dt.month
        df["day"] = df[date_column].dt.day
        df["dayofweek"] = df[date_column].dt.dayofweek

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows.
    """
    return df.drop_duplicates()


def handle_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle outliers using IQR method (for numerical columns).
    """
    numeric_cols = df.select_dtypes(include=np.number).columns

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
        df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])

    return df


def preprocess_data(file_path: str, date_column: str = "date") -> pd.DataFrame:
    """
    Full preprocessing pipeline.
    """
    df = load_data(file_path)
    df = standardize_column_names(df)
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = convert_datetime(df, date_column)
    df = handle_outliers(df)

    return df


def save_processed_data(df: pd.DataFrame, output_path: str):
    """
    Save cleaned dataset to CSV.
    """
    try:
        df.to_csv(output_path, index=False)
        print(f"Processed data saved at: {output_path}")
    except Exception as e:
        raise Exception(f"Error saving data: {e}")
