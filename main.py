import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g, session
from io import BytesIO
from database import setup, stock, projects, convert, extractor
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

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

@app.route('/home/<project_name>', methods=['GET', 'POST'])
def project_page(project_name):
    conn = get_db()
    
    project_floss = projects.list_project_details(conn, project_name)
    
    if request.method == 'POST':
        action = request.form['button']
        
        if action == "delete-project":
            projects.delete_project(conn, project_name)
            return redirect(url_for('home_page'))
        
        elif action == "amend-project":
            return redirect(url_for('home_page'))
            # return redirect(url_for('amend_project', project_name=project_name))
            
    return render_template('project_page.html', project_name = project_name, project_floss=project_floss)

# New project page
@app.route('/new-project', methods=['GET', 'POST'])
def project_setup():
    error = session.get('error', '')
    floss_list = session.get('floss_list', [])
    project_name = session.get('project_name', '')
    start_date = session.get('start_date', '')

    if request.method == 'POST':
        conn = get_db()       
        action = request.form['button']
        
        # Store session data
        session['project_name'] = request.form['project-name']
        session['start_date'] = request.form['start-date']
        pattern_file = request.files['file']
        
        # Uploading PDF for floss extraction
        if action == 'upload': 
            if pattern_file.filename == '':
                return redirect(url_for('project_setup'))

            if pattern_file and pattern_file.filename.lower().endswith('.pdf'):
                session['floss_list'] = extractor.extract_floss(BytesIO(pattern_file.read()))
                
                return redirect(url_for('project_setup'))

        # Creating project
        if action == 'create':
            # Checks that required fields are filled
            if not request.form['project-name'] or not request.form['start-date']:
                session['error'] = f'Please input relevant details!'
                return redirect(url_for('project_setup'))
            
            # Checks that project is not already existing
            if projects.search_project(conn, request.form['project-name']):
                session['error'] = f'Project already exists!'
                return redirect(url_for('project_setup'))
            
            else:
                # Create project and details
                projects.create_project(conn, session['project_name'], session['start_date'])

                # Retrieve all from 'floss-item' input fields
                floss_items = request.form.getlist('floss-item') 
                for f in floss_items:
                    if setup.validate_floss_input(f):
                        brand, fno = setup.fix_input(f)
                        projects.project_add_floss(conn, session['project_name'], brand, fno)
                
                project_name=session['project_name']
                session.clear()
                return redirect(url_for('project_page', project_name=project_name))
    
    return render_template('project_setup.html', 
                           floss_list=floss_list, 
                           project_name=project_name, 
                           start_date=start_date,
                           error=error)

# # Amend project details page
# @app.route('/amend-project/<project-name>/', methods=['GET', 'POST'])
# def amend_project(project_name):
#     conn = get_db()
    
#     return render_template('amend_project.html', )
    
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