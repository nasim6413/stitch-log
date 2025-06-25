from flask import Blueprint, render_template, session, request, redirect, url_for
from stitchlog.models import setup, projects, extractor
from io import BytesIO

p = Blueprint('projects', __name__, url_prefix='/projects')

@p.route('/')
def projects_home():
    conn = setup.get_db()
    session.clear()
    
    projects_list = projects.list_projects(conn)
    
    return render_template('home.html', projects_list=projects_list)

# Project page
@p.route('/<project_name>', methods=['GET', 'POST'])
def project_page(project_name):
    conn = setup.get_db()
    session.clear()

    project_floss = projects.list_project_details(conn, project_name)
    
    if request.method == 'POST':
        action = request.form['button']
        
        if action == "delete-project":
            projects.project_del_all_floss(conn, project_name)
            projects.delete_project(conn, project_name)

            return redirect(url_for('projects_home'))
        
        elif action == "amend-project":
            return redirect(url_for('projects.floss_setup', project_name=project_name))
            
    return render_template('project_page.html', project_name=project_name, project_floss=project_floss)

# New project page
@p.route('/new', methods=['GET', 'POST'])
def project_setup():
    error = session.get('error', '')
    project_name = session.get('project_name', '')
    start_date = session.get('start_date', '')

    if request.method == 'POST':
        conn = setup.get_db()       
        action = request.form['button']
        
        # Store session data
        session['project_name'] = project_name = request.form['project-name']
        session['start_date'] = start_date = request.form['start-date']

        # Creating project
        if action == 'create':

            # Checks that required fields are filled
            if not project_name or not start_date:
                session['error'] = f'Please input relevant details!'
                return redirect(url_for('projects.project_setup'))
            
            # Checks that project is not already existing
            if projects.search_project(conn, project_name):
                session['error'] = f'Project already exists!'
                return redirect(url_for('projects.project_setup'))
            
            else:
                # Create project and details
                projects.create_project(conn, project_name, start_date)

                session.clear()
                return redirect(url_for('projects.floss_setup', project_name=project_name))
    
    return render_template('project_setup.html', 
                           project_name=project_name, 
                           start_date=start_date,
                           error=error)

# Project floss page
@p.route('/<project_name>/floss', methods=['GET', 'POST'])
def floss_setup(project_name):
    conn = setup.get_db()

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
                return redirect(url_for('projects.floss_setup', project_name=project_name))

            if pattern_file and pattern_file.filename.lower().endswith('.pdf'):
                floss_extracted = extractor.extract_floss(BytesIO(pattern_file.read()))

                # Merge existing + new floss entries
                floss_list.extend(floss_extracted)
                
                session['floss_list'] = floss_list

                return redirect(url_for('projects.floss_setup', project_name=project_name))
        
        # Add more floss fields
        if action == 'add-floss':
            floss_items = request.form.getlist('floss-item')
            floss_list = [tuple(item.strip().split()) for item in floss_items]

            floss_list.append((' ', ' '))

            session['floss_list'] = floss_list

            return redirect(url_for('projects.floss_setup', project_name=project_name))

        # Submit final data
        if action == 'submit-floss':

            # Retrieve all from 'floss-item' input fields
            floss_items = request.form.getlist('floss-item')

            # Deletes current floss in project_details
            projects.project_del_all_floss(conn, project_name)

            for f in floss_items:
                f = f.strip() # Floss added by user will have whitespace
                
                if setup.validate_floss_input(f):
                    brand, fno = setup.fix_input(f)
                    projects.project_add_floss(conn, project_name, brand, fno)

            session.clear()
            return redirect(url_for('projects.project_page', project_name=project_name))
        
    return render_template('floss_setup.html', floss_list=floss_list, project_name=project_name)