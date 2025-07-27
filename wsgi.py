import sys
from pathlib import Path

# Add your project directory to the path
project_home = str(Path(__file__).parent)
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Import and run the Flask application instance
from app import app as application