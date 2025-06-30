from flask import Blueprint, render_template, session, request, redirect, url_for
from stitchlog.models import setup, projects, extractor, floss
from io import BytesIO
from datetime import datetime, date

p = Blueprint('projects', __name__, url_prefix='/projects')

@p.route('/')
def projects_home():
    conn = setup.get_db()

    projects_list = projects.list_project_details(conn)
    
    return render_template('project_list.html', projects_list=projects_list)

# Project page
@p.route('/<project_name>', methods=['GET', 'POST'])
def project_page(project_name):
    conn = setup.get_db()
    data = {}

    project_floss = projects.list_project_floss(conn, project_name)
    project_details = projects.list_project_details(conn, project_name)[0]

    # Populate dict of data
    data['project_name'] = project_name
    data['project_date'] = project_details[1] # Project start date

    start_date_obj = datetime.strptime(data['project_date'], "%Y-%m-%d").date() # Convert to datetime
    end_date_str = project_details[-2]

    # Convert end_date_str to a date if it's not empty, otherwise use today's date
    if end_date_str:
        end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    else:
        end_date_obj = date.today()

    data['project_days'] = (end_date_obj - start_date_obj).days
    data['project_prog'] = project_details[-1]
    
    if request.method == 'POST':
        action = request.form['button']

        if action == "delete-project":
            projects.project_del_all_floss(conn, project_name)
            projects.delete_project(conn, project_name)

            return redirect(url_for('projects.projects_home'))
        
        elif action == "amend-project":
            return redirect(url_for('projects.project_setup', project_name=project_name))
            
    return render_template('project_page.html', project_floss=project_floss, data=data)

# Project details page
@p.route('/<project_name>/details-setup', methods=['GET', 'POST'])
@p.route('/new', methods=['GET', 'POST'])
def project_setup(project_name = None):
    conn = setup.get_db()   
    data = {}

    if project_name: # Edit case loads existing project data
        project = projects.list_project_details(conn, project_name)[0]

        if project:
            # Populate data from the database
            data['button'] = 'Update'
            data['project_name'] = project_name
            data['start_date'] = project[1]
            data['end_date'] = project[2] or ''
            data['progress'] = project[-1] or ''
            data['button'] = 'Update'

    else:
        data['button'] = 'Create'

    # Override data with session data
    data['error'] = session.pop('error', '')
    data['project_name'] = session.pop('project_name', data.get('project_name', ''))
    data['start_date'] = session.pop('start_date', data.get('start_date', ''))
    data['end_date'] = session.pop('end_date', data.get('end_date', ''))
    data['progress'] = int(session.pop('progress', data.get('progress', 1) or 1))

    if request.method == 'POST':
           
        action = request.form['button'].lower()
        
        # Collect form data
        form_project_name = session['project_name'] = request.form['project-name']
        form_start_date = session['start_date'] = request.form['start-date']
        form_end_date = session['end_date'] = request.form.get('end-date', '')
        form_progress = session['progress'] = int(request.form.get('progress', 1) or 1)

        # Validation check for required fields
        if not form_project_name or not form_start_date:
            session['error'] = 'Please input relevant details!'
            return redirect(url_for('projects.project_setup', project_name=project_name))

        # Data validation
        val_start_date = datetime.strptime(form_start_date, "%Y-%m-%d").date()

        if form_end_date:
            val_end_date = datetime.strptime(form_end_date, "%Y-%m-%d").date()
        else:
            val_end_date = date.today()

        if val_start_date > date.today() or val_end_date < val_start_date:
            session['error'] = f'Please input valid start and/or end dates!'
            return redirect(url_for('projects.project_setup', project_name=project_name))
        
        if (form_end_date and form_progress < 100) or (form_progress == 100 and not form_end_date):
            session['error'] = f'Please update completion information.'
            return redirect(url_for('projects.project_setup', project_name=project_name))


        if action == 'create':
            # Validation check whether project exists already
            if projects.list_project_details(conn, form_project_name):
                session['error'] = 'Project already exists!'
                return redirect(url_for('projects.project_setup'))
            
            # Else creates project
            else:
                projects.create_project(conn, form_project_name, form_start_date, form_end_date, form_progress)
                return redirect(url_for('projects.floss_setup', project_name=form_project_name))

        elif action == 'update':
            # Updates project details
            projects.update_project(conn, form_project_name, form_end_date)
            projects.update_project_progress(conn, form_project_name, form_progress)

            return redirect(url_for('projects.floss_setup', project_name=form_project_name))

    return render_template('project_setup.html', data=data)

# Project floss page
@p.route('/<project_name>/floss-setup', methods=['GET', 'POST'])
def floss_setup(project_name):
    conn = setup.get_db()

    floss_list = session.pop('floss_list', []) # Gets floss_list in session

    # If not a list/tuple, try fetching from DB
    if not floss_list:
        floss_list = projects.list_project_floss(conn, project_name)
    
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
                brand, fno = floss.fix_floss_input(f)

                if brand and fno:
                    projects.project_add_floss(conn, project_name, brand, fno)

            return redirect(url_for('projects.project_page', project_name=project_name))
        
    return render_template('floss_setup.html', floss_list=floss_list, project_name=project_name)