from flask import Flask
from config.config import config_dict


def create_app(env="development"):
    """
    Flask Application Factory
    """
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_dict[env])

    # Register Blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
