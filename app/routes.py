from flask import Blueprint, render_template, request, current_app
import pandas as pd
import os

# Import your modules
from src.data_preprocessing import preprocess_data
from src.eda import generate_all_plots
from src.model import load_model, predict
from src.utils import categorize_aqi, align_features, load_pickle

main = Blueprint("main", __name__)


# ==============================
# HOME ROUTE
# ==============================
@main.route("/")
def home():
    return render_template("index.html")


# ==============================
# ANALYSIS ROUTE
# ==============================
@main.route("/analysis")
def analysis():
    """
    Generate EDA plots and display them
    """
    data_path = current_app.config["PROCESSED_DATA_PATH"]
    output_dir = current_app.config["FIGURES_DIR"]

    # Load data
    df = pd.read_csv(data_path)

    # Generate plots
    generate_all_plots(df, output_dir)

    # Pass image filenames to template
    images = os.listdir(output_dir)

    return render_template("analysis.html", images=images)


# ==============================
# PREDICTION ROUTE
# ==============================
@main.route("/predict", methods=["GET", "POST"])
def predict_route():
    """
    Handle AQI prediction
    """
    if request.method == "POST":
        try:
            # ------------------------------
            # Load model & feature columns
            # ------------------------------
            model_path = current_app.config["MODEL_PATH"]
            model = load_model(model_path)

            feature_path = os.path.join(
                current_app.config["MODEL_DIR"], "features.pkl"
            )
            feature_columns = load_pickle(feature_path)

            # ------------------------------
            # Get user input
            # ------------------------------
            input_data = {}

            for key, value in request.form.items():
                try:
                    input_data[key] = float(value)
                except ValueError:
                    input_data[key] = 0

            input_df = pd.DataFrame([input_data])

            # ------------------------------
            # Align features
            # ------------------------------
            input_df = align_features(input_df, feature_columns)

            # ------------------------------
            # Predict
            # ------------------------------
            prediction = predict(model, input_df)

            # Categorize AQI
            category = categorize_aqi(prediction)

            return render_template(
                "prediction.html",
                prediction=round(prediction, 2),
                category=category
            )

        except Exception as e:
            return render_template(
                "prediction.html",
                error=str(e)
            )

    return render_template("prediction.html")
