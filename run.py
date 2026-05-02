import os
from app import create_app

# Get environment (default = development)
env = os.environ.get("FLASK_ENV", "development")

# Create Flask app instance
app = create_app(env)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",   # accessible externally
        port=5000,
        debug=app.config.get("DEBUG", False)
    )
