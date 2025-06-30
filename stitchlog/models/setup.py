import pandas as pd
import os
import sqlite3
from flask import g, current_app
from ..utils import *

def set_up(conn):   
    
    """Performs first-time setup for database."""
    
    cursor = conn.cursor()
         
    # Conversion tables
    cursor.execute("""
        CREATE TABLE dmc_to_anchor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dmc TEXT NOT NULL,
        anchor TEXT NOT NULL,
        hex TEXT,
        colour TEXT
        );
    """)
    
    cursor.execute("""
        CREATE TABLE anchor_to_dmc (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        anchor TEXT NOT NULL,
        dmc TEXT NOT NULL,
        hex TEXT,
        colour TEXT
        );
    """)
    
    # Stock table
    cursor.execute("""
        CREATE TABLE stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            fno TEXT NOT NULL
        );
    """)
    
    # Projects table
    cursor.execute("""
        CREATE TABLE project_details (
            project_name TEXT NOT NULL PRIMARY KEY,
            start_date TIMESTAMP NOT NULL,
            end_date TIMESTAMP,
            progress NOT NULL
        );
    """)
    
    # Project floss table
    cursor.execute("""
        CREATE TABLE project_floss (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            brand TEXT NOT NULL,
            fno TEXT NOT NULL
        );
    """)
    
    # Retrieving conversion data
    dmc_to_anchor = pd.read_csv('data/dmc_to_anchor.csv', names=['dmc', 'anchor', 'hex', 'colour'])
    dmc_to_anchor = dmc_to_anchor[dmc_to_anchor.anchor != 'NA']
            
    anchor_to_dmc = pd.read_csv('data/anchor_to_dmc.csv', names=['anchor', 'dmc', 'hex', 'colour'])
    anchor_to_dmc = anchor_to_dmc[anchor_to_dmc.dmc != 'NA']
    
    # Populate conversion tables
    dmc_to_anchor.to_sql('dmc_to_anchor', conn, if_exists='append', index = False)
    anchor_to_dmc.to_sql('anchor_to_dmc', conn, if_exists='append', index = False)
    
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
