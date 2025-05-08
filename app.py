# Entry point for the Finance Planner app

from app import create_app
from app.config import Config

# Create the Flask app instance with the configuration
app = create_app()
app.config.from_object(Config)
app.config['DEBUG'] = True  # Enable debug mode for development

if __name__ == "__main__":
    # Run the app in debug mode for development
    app.run(debug=True)