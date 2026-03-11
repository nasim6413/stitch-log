import csv
import os
import sqlite3
from flask import g, current_app
from ..utils.utils import *

def set_up(conn):   
    
    """Performs first-time setup for database."""
    
    cursor = conn.cursor()
         
    # Conversion tables
    cursor.execute("""
        CREATE TABLE conversions (
        conversion_id INTEGER PRIMARY KEY AUTOINCREMENT,
        dmc TEXT NOT NULL,
        anchor TEXT NOT NULL,
        hex TEXT NOT NULL,
        colour TEXT NOT NULL
        );
        """)
    
    # Stock table
    cursor.execute("""
        CREATE TABLE stock (
            stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            f_no TEXT NOT NULL
        );
        """)
    
    # Projects table
    cursor.execute("""
        CREATE TABLE projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            start_date TIMESTAMP NOT NULL,
            end_date TIMESTAMP
        );
        """)
    
    # Project floss table
    cursor.execute("""
        CREATE TABLE project_floss (
            floss_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            brand TEXT NOT NULL,
            f_no TEXT NOT NULL
        );
        """)
    
    # Read and insert conversion data
    with open('stitchlog/data/conversions.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) # skip first row
        
        for row in reader:
            cursor.execute(
                """
                INSERT INTO conversions (dmc, anchor, hex, colour) 
                VALUES (?, ?, ?, ?)
                """,
                (row[0], row[1], row[2], row[3])
            )
    
    return

def get_db():
    
    """Connecting to database within Flask app."""
    
    if 'db' not in g:
        # Configures database path from app's config, not hardcoded
        g.db = sqlite3.connect(current_app.config['DATABASE'])
    return g.db

def close_db(e=None):
    
    """Closing database connection within Flask app."""
    
    db = g.pop('db', None)
    if db is not None:
        db.close()

def get_username():

    """Access the USERNAME from app config."""
    
    username = current_app.config.get('USERNAME', None)

    return username

def set_username(app, username):

    """Set the USERNAME in instance/config.py."""

    config_path = os.path.join(app.instance_path, 'config.py')

    try: 
        with open(config_path, 'a') as f:
            f.write(f'\nUSERNAME = "{username}"\n')

        app.config.from_pyfile('config.py', silent=True)  # Reload config

        return True
    
    except:
        return False
