import os
import sys

# Add the project root directory to Python's sys.path
# This is required because Vercel runs this file with the `api/` directory as the working directory,
# making the root-level `app` module undiscoverable by default.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

# This is the entrypoint for Vercel Serverless Functions.
