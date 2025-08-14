# # src/config.py
# YOUTUBE_API_KEY = "AIzaSyD9KCJ2z_UbGzzey3TooMI6ryfC64ofYLs"
# YOUTUBE_API_SERVICE_NAME = "youtube"
# YOUTUBE_API_VERSION = "v3"

# DB_URL = "sqlite:///../database/youtube.db"  # or your PostgreSQL URI
# src/config.py
import os

YOUTUBE_API_KEY = "AIzaSyD9KCJ2z_UbGzzey3TooMI6ryfC64ofYLs"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Dynamically generate absolute path to database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # path to 'src' folder
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "database", "youtube.db"))
DB_URL = f"sqlite:///{DB_PATH}"