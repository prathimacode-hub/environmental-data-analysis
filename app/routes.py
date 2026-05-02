from flask import Blueprint, render_template, current_app
import pandas as pd
import os

# Forms
from .forms import AQIPredictionForm

# Core modules
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
    Generate and display EDA plots
    """
    data_path = current_app.config["PROCESSED_DATA_PATH"]
    output_dir = current_app.config["FIGURES_DIR"]

    # Load dataset
    df = pd.read_csv(data_path)

    # Generate plots
    generate_all_plots(df, output_dir)

    # Get image list
    images = os.listdir(output_dir)

    return render_template("analysis.html", images=images)


# ==============================
# PREDICTION ROUTE
# ==============================
@main.route("/predict", methods=["GET", "POST"])
def predict_route():
    """
    Handle AQI prediction using Flask-WTF form
    """
    form = AQIPredictionForm()

    if form.validate_on_submit():
        try:
            # ------------------------------
            # Load model
            # ------------------------------
            model_path = current_app.config["MODEL_PATH"]
            model = load_model(model_path)

            # ------------------------------
            # Load feature columns
            # ------------------------------
            feature_path = os.path.join(
                current_app.config["MODEL_DIR"], "features.pkl"
            )
            feature_columns = load_pickle(feature_path)

            # ------------------------------
            # Collect input data from form
            # ------------------------------
            input_data = {
                "pm25": form.pm25.data,
                "pm10": form.pm10.data,
                "no2": form.no2.data or 0,
                "so2": form.so2.data or 0,
                "co": form.co.data or 0,
                "o3": form.o3.data or 0,
                "month": form.month.data or 0,
                "dayofweek": form.dayofweek.data or 0,
            }

            input_df = pd.DataFrame([input_data])

            # ------------------------------
            # Align features with training
            # ------------------------------
            input_df = align_features(input_df, feature_columns)

            # ------------------------------
            # Prediction
            # ------------------------------
            prediction = predict(model, input_df)
            category = categorize_aqi(prediction)

            return render_template(
                "prediction.html",
                form=form,
                prediction=round(prediction, 2),
                category=category
            )

        except Exception as e:
            return render_template(
                "prediction.html",
                form=form,
                error=str(e)
            )

    return render_template("prediction.html", form=form)

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
