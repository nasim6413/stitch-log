import os

# Base directory of your project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Path to SQLite DB in instance folder
DATABASE = os.path.join(BASE_DIR, 'instance', 'floss.db') 

# Default (non-secret) key — override in instance/config.py
SECRET_KEY = 'dev'