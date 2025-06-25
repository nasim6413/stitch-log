import os
from flask import Flask
from stitchlog.models import setup

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_object('config')
    app.config.from_pyfile('config.py', silent=True)
    app.teardown_appcontext(setup.close_db)
    
    # Ensures instanace file exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Perform first-time setup
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
    from stitchlog.views import projects, stock, convert
    app.register_blueprint(projects.p)
    app.register_blueprint(stock.s)
    app.register_blueprint(convert.c)

    return app