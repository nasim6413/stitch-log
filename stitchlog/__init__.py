import os
from flask import Flask
from stitchlog.models import setup

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Ensures instance file exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Creates a secret key if one doesn't exist
    secret_key_path = os.path.join(app.instance_path, 'config')
    if not os.path.exists(secret_key_path):
        with open(secret_key_path, 'wb') as f:
            f.write(os.urandom(24))

    app.config.from_object('config') # Base config.py
    app.config.from_pyfile('config.py', silent=True) # instance/config.py will override

    # Load the generated or existing key
    with open(secret_key_path, 'rb') as f:
        app.config['SECRET_KEY'] = f.read()

    app.teardown_appcontext(setup.close_db)
    
    # First-time database setup
    with app.app_context():
        conn = setup.get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            setup.set_up(conn)

        conn.commit()
        cursor.close()
        conn.close()

    # Register blueprints
    from stitchlog.views import projects, stock, convert, home
    app.register_blueprint(home.h)
    app.register_blueprint(projects.p)
    app.register_blueprint(stock.s)
    app.register_blueprint(convert.c)

    return app