import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set global style
sns.set(style="whitegrid")


def create_output_dir(path: str):
    """
    Create directory if it doesn't exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def plot_aqi_distribution(df: pd.DataFrame, output_path: str = None):
    """
    Plot AQI distribution.
    """
    plt.figure()
    sns.histplot(df['aqi'], bins=50, kde=True)
    plt.title("AQI Distribution")
    plt.xlabel("AQI")
    plt.ylabel("Frequency")

    if output_path:
        plt.savefig(output_path, bbox_inches='tight')
    else:
        plt.show()

    plt.close()


def plot_aqi_trend(df: pd.DataFrame, date_column: str = "date", output_path: str = None):
    """
    Plot AQI trend over time.
    """
    if date_column not in df.columns:
        raise ValueError(f"{date_column} column not found")

    df_sorted = df.sort_values(by=date_column)

    plt.figure()
    plt.plot(df_sorted[date_column], df_sorted['aqi'])
    plt.title("AQI Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("AQI")

    if output_path:
        plt.savefig(output_path, bbox_inches='tight')
    else:
        plt.show()

    plt.close()


def plot_correlation_heatmap(df: pd.DataFrame, output_path: str = None):
    """
    Plot correlation heatmap for numerical features.
    """
    plt.figure(figsize=(10, 8))
    corr = df.corr(numeric_only=True)

    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap")

    if output_path:
        plt.savefig(output_path, bbox_inches='tight')
    else:
        plt.show()

    plt.close()


def plot_pollutants_vs_aqi(df: pd.DataFrame, output_path: str = None):
    """
    Scatter plots of pollutants vs AQI.
    """
    pollutant_cols = [col for col in df.columns if col not in ['aqi', 'date']]

    for col in pollutant_cols:
        if df[col].dtype in ['float64', 'int64']:
            plt.figure()
            sns.scatterplot(x=df[col], y=df['aqi'])
            plt.title(f"{col} vs AQI")
            plt.xlabel(col)
            plt.ylabel("AQI")

            if output_path:
                file_name = f"{col}_vs_aqi.png"
                plt.savefig(os.path.join(output_path, file_name), bbox_inches='tight')
            else:
                plt.show()

            plt.close()


def plot_aqi_by_category(df: pd.DataFrame, category_column: str = "aqi_category", output_path: str = None):
    """
    Plot AQI category distribution (if available).
    """
    if category_column not in df.columns:
        return

    plt.figure()
    sns.countplot(x=df[category_column])
    plt.title("AQI Category Distribution")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.xticks(rotation=45)

    if output_path:
        plt.savefig(output_path, bbox_inches='tight')
    else:
        plt.show()

    plt.close()


def generate_all_plots(df: pd.DataFrame, output_dir: str):
    """
    Generate and save all EDA plots.
    """
    create_output_dir(output_dir)

    plot_aqi_distribution(df, os.path.join(output_dir, "aqi_distribution.png"))
    plot_aqi_trend(df, output_path=os.path.join(output_dir, "aqi_trend.png"))
    plot_correlation_heatmap(df, os.path.join(output_dir, "correlation_heatmap.png"))
    plot_pollutants_vs_aqi(df, output_dir)
    plot_aqi_by_category(df, output_path=os.path.join(output_dir, "aqi_category.png"))
