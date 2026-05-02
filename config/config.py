import os

class Config:
    """Base configuration (common for all environments)"""

    # Project root
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Secret key (important for sessions/forms)
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key")

    # Data paths
    DATA_DIR = os.path.join(BASE_DIR, "data")
    RAW_DATA_PATH = os.path.join(DATA_DIR, "raw", "environmental_analysis.csv")
    PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed", "cleaned_aqi_data.csv")

    # Model path
    MODEL_DIR = os.path.join(BASE_DIR, "models")
    MODEL_PATH = os.path.join(MODEL_DIR, "trained_model.pkl")

    # Output paths
    OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
    FIGURES_DIR = os.path.join(OUTPUT_DIR, "figures")
    REPORTS_DIR = os.path.join(OUTPUT_DIR, "reports")

    # Uploads (if needed)
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload

    # Flask configs
    DEBUG = False
    TESTING = False

    # Logging
    LOG_LEVEL = "INFO"


class DevelopmentConfig(Config):
    """Development environment"""

    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production environment"""

    DEBUG = False
    LOG_LEVEL = "WARNING"


class TestingConfig(Config):
    """Testing environment"""

    TESTING = True
    DEBUG = True
    LOG_LEVEL = "DEBUG"


# Config dictionary for easy access
config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
