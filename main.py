import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g
from markupsafe import escape
from database import setup, stock, projects, convert

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('floss.db')
    return g.db
    
@app.route('/')
@app.route('/home')
def home_page():
    conn = get_db()
    
    projects_list = projects.list_projects(conn)
    
    return render_template('home.html', projects_list=projects_list)

@app.route('/home/<project_name>')
def show_project(project_name):
    
    return render_template('project_page.html', project_name = project_name)

# New project page
@app.route('/new-project', methods=['GET', 'POST'])
def new_project_page():
    if request.method == 'POST':
        conn = get_db()
        
        project_name = request.form['project-name']
        start_date = request.form['start-date']
        
        projects.create_project(conn, project_name, start_date)
        
        return redirect(url_for('home_page'))
    
    return render_template('new_project.html')

# Stock page
@app.route('/stock', methods=['GET', 'POST'])
def stock_page():
    conn = get_db()
    
    if request.method == 'POST':
        item = request.form['floss']
        
        if setup.validate_floss_input(item):
            brand, fno = setup.fix_input(item)
            action = request.form['button']
            
            if action == 'add':
                stock.stock_add(conn, brand, fno)
            if action == 'delete':
                stock.stock_del(conn, brand, fno)
            
            return redirect(url_for('stock_page'))
        
        else:
            return redirect(url_for('stock_page'))
        
    rows = stock.stock_list(conn)
    return render_template('stock.html', rows=rows)

# Conversion page
@app.route('/convert', methods=['GET', 'POST'])
def convert_page():
    conn = get_db()
    
    if request.method == 'POST':
        item = request.form['floss']
        
        if setup.validate_floss_input(item):
            brand, fno = setup.fix_input(item)
                                   
            converted_brand, rows = convert.gen_convert(conn, brand, fno)
                
            return render_template('convert.html', brand=brand, converted_brand=converted_brand, rows=rows)
        
        else:
            return redirect(url_for('convert_page'))
    
    return render_template('convert.html')

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close()

if __name__ == '__main__':
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            setup.set_up(conn)

        conn.commit()
        cursor.close()
        conn.close()
        
    app.run()