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
    session.clear()
    
    projects_list = projects.list_projects(conn)
    
    return render_template('home.html', projects_list=projects_list)

# Project page
@app.route('/home/<project_name>', methods=['GET', 'POST'])
def project_page(project_name):
    conn = get_db()
    session.clear()

    project_floss = projects.list_project_details(conn, project_name)
    
    if request.method == 'POST':
        action = request.form['button']
        
        if action == "delete-project":
            projects.project_del_all_floss(conn, project_name)
            projects.delete_project(conn, project_name)

            return redirect(url_for('home_page'))
        
        elif action == "amend-project":
            return redirect(url_for('floss_setup', project_name=project_name))
            
    return render_template('project_page.html', project_name=project_name, project_floss=project_floss)

# New project page
@app.route('/new-project', methods=['GET', 'POST'])
def project_setup():
    error = session.get('error', '')
    project_name = session.get('project_name', '')
    start_date = session.get('start_date', '')

    if request.method == 'POST':
        conn = get_db()       
        action = request.form['button']
        
        # Store session data
        session['project_name'] = project_name = request.form['project-name']
        session['start_date'] = start_date = request.form['start-date']

        # Creating project
        if action == 'create':

            # Checks that required fields are filled
            if not project_name or not start_date:
                session['error'] = f'Please input relevant details!'
                return redirect(url_for('project_setup'))
            
            # Checks that project is not already existing
            if projects.search_project(conn, project_name):
                session['error'] = f'Project already exists!'
                return redirect(url_for('project_setup'))
            
            else:
                # Create project and details
                projects.create_project(conn, project_name, start_date)

                session.clear()
                return redirect(url_for('floss_setup', project_name=project_name))
    
    return render_template('project_setup.html', 
                           project_name=project_name, 
                           start_date=start_date,
                           error=error)

# Project floss page
@app.route('/projects/<project_name>/floss', methods=['GET', 'POST'])
def floss_setup(project_name):
    conn = get_db()

    floss_list = session.get('floss_list', []) # Gets floss_list in session

    # If not a list/tuple, try fetching from DB
    if not floss_list:
        floss_list = projects.list_project_details(conn, project_name)
    
    # If still not a list/tuple, force empty list
    if not floss_list:
        floss_list = []
    
    if request.method == 'POST':      
        action = request.form['button']

        # Uploading PDF for floss extraction
        if action == 'upload': 
            pattern_file = request.files['file']

            floss_items = request.form.getlist('floss-item')
            floss_list = [tuple(item.strip().split()) for item in floss_items] #Convert to list of tuples

            if pattern_file.filename == '':
                return redirect(url_for('project_setup'))

            if pattern_file and pattern_file.filename.lower().endswith('.pdf'):
                floss_extracted = extractor.extract_floss(BytesIO(pattern_file.read()))

                # Merge existing + new floss entries
                floss_list.extend(floss_extracted)
                
                session['floss_list'] = floss_list

                return redirect(url_for('floss_setup', project_name=project_name))
        
        # Add more floss fields
        if action == 'add-floss':
            floss_items = request.form.getlist('floss-item')
            floss_list = [tuple(item.strip().split()) for item in floss_items]

            floss_list.append((' ', ' '))

            session['floss_list'] = floss_list

            return redirect(url_for('floss_setup', project_name=project_name))

        # Submit final data
        if action == 'submit-floss':

            # Retrieve all from 'floss-item' input fields
            floss_items = request.form.getlist('floss-item')

            # Deletes current floss in project_details
            projects.project_del_all_floss(conn, project_name)

            for f in floss_items:
                if setup.validate_floss_input(f):
                    brand, fno = setup.fix_input(f)
                    projects.project_add_floss(conn, project_name, brand, fno)

            session.clear()
            return redirect(url_for('project_page', project_name=project_name))
        
    return render_template('floss_setup.html', floss_list=floss_list, project_name=project_name)
    
# Stock page
@app.route('/stock', methods=['GET', 'POST'])
def stock_page():
    conn = get_db()
    session.clear()
    
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
    session.clear()
    
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