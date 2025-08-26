from flask import Blueprint, render_template, request
from stitchlog.models import setup, projects, extractor, floss
from datetime import datetime, date
from ..utils.search import search_project, search_project_floss
from ..utils.responses import *

p = Blueprint('projects', __name__, url_prefix='/projects')

@p.route('/')
def projects_home():   
    return render_template('projects_page.html')

@p.route('/<project_name>', methods=['GET'])
def project_page(project_name):
    return render_template('project_details.html')

@p.route('/new-project')
def project_setup():
    return render_template('project_setup.html')

# Retrieving project lists/details
@p.route('/list', methods=['GET'])
def projects_list():
    conn = setup.get_db()
    rows = projects.list_all_projects(conn)
    return success_response([
        {
        "project_name" : r[0],
        "project_progress" : r[1]
        } for r in rows
    ]) if rows else error_response("Error in retrieving project list.")

@p.route('/<project_name>/details', methods=['GET'])
def project_page_details(project_name):
    conn = setup.get_db()
    
    if search_project(conn, project_name):
        details = projects.list_project_details(conn, project_name)

        return success_response(details) if details else error_response("There a problem in retrieving the project details.")
    
    else:
        return error_response("Project does not exist!")

# Project creation
@p.route('/new-project/create', methods=['POST'])
def project_creation():
    conn = setup.get_db()
    data = request.get_json()
    
    # Checks that project is not already existing
    if not search_project(conn, data['project_name']):
        result = projects.create_project(conn, data['project_name'], data['start_date'], data['end_date'], data['progress'])
        
        # Successful project creation
        return success_response() if result else error_response("Error in creating project.")
            
    else:
        return error_response("Project already exists!")
            
# Project deletion (project AND floss)
@p.route('/<project_name>/delete', methods=['POST'])
def project_delete(project_name):
    conn = setup.get_db()
    
    # Checks that project exists
    if search_project(conn, project_name):
        result_project = projects.delete_project(conn, project_name)
        result_floss = projects.project_del_all_floss(conn, project_name)
        
        # Successful project and floss deletions
        return success_response() if result_project and result_floss else error_response("Error when deleting project!")
            
    else:
        return error_response("Project does not exist!")
    
# Project retrieve floss from PDF
@p.route('/<project_name>/extract', methods=['GET', 'POST'])
def project_floss_extractor(project_name):
        if "file" not in request.files:
            return error_response("No file uploaded.")

        # Uploading PDF for floss extraction
        pattern_file = request.files['file']
        if extractor.validate_upload(pattern_file):
            extracted_floss = extractor.extract_floss(pattern_file)

            return success_response(extracted_floss) if extracted_floss else error_response("Error in floss extraction.")
            
        else:
            return error_response("Invalid file input!")
        
@p.route('/<project_name>/floss', methods=['GET'])
def project_page_floss(project_name):
    conn = setup.get_db()

    if search_project(conn, project_name):
        rows = projects.list_project_floss(conn, project_name)

        return success_response([{
            "brand" : r[0],
            "fno" : r[1],
            "availability" : r[2]
        } for r in rows
        ]) if rows else error_response("No floss associated with project.")
        
    else:
        return error_response("Project does not exist!")
    
@p.route('/<project_name>/floss/add', methods=['POST'])
def project_add_floss(project_name):
    conn = setup.get_db()
    data = request.get_json()
    item = data.get('floss', '').strip()

    brand, fno = floss.fix_floss_input(item)

    if not search_project_floss(conn, project_name, brand, fno):
        result = projects.project_add_floss(conn, project_name, brand, fno)

        return success_response() if result else error_response("Error adding floss to project.")
    
    else:
        return error_response("Floss already in project.")


@p.route('/<project_name>/floss/delete', methods=['POST'])
def project_del_floss(project_name):
    conn = setup.get_db()
    data = request.get_json()
    item = data.get('floss', '').strip()

    brand, fno = floss.fix_floss_input(item)

    if search_project_floss(conn, project_name, brand, fno):
        result = projects.project_delete_floss

        return success_response() if result else error_response("Error deleting floss from project.")
    
    else:
        return error_response("Floss not in project.")



# Project amend details

# Project amend floss


# # Project page
# @p.route('/<project_name>', methods=['GET', 'POST'])
# def project_page(project_name):
#     conn = setup.get_db()
#     data = {}

#     project_floss = projects.list_project_floss(conn, project_name)
#     project_details = projects.list_project_details(conn, project_name)[0]

#     # Populate dict of data
#     data['project_name'] = project_name
#     data['project_date'] = project_details[1] # Project start date

#     start_date_obj = datetime.strptime(data['project_date'], "%Y-%m-%d").date() # Convert to datetime
#     end_date_str = project_details[-2]

#     # Convert end_date_str to a date if it's not empty, otherwise use today's date
#     if end_date_str:
#         end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d").date()
#     else:
#         end_date_obj = date.today()

#     data['project_days'] = (end_date_obj - start_date_obj).days
#     data['project_prog'] = project_details[-1]
    
#     if request.method == 'POST':
#         action = request.form['button']

#         if action == "delete-project":
#             projects.project_del_all_floss(conn, project_name)
#             projects.delete_project(conn, project_name)

#             return redirect(url_for('projects.projects_home'))
        
#         elif action == "amend-project":
#             return redirect(url_for('projects.project_setup', project_name=project_name))
            
#     return render_template('project_page.html', project_floss=project_floss, data=data)

# # Project details page
# @p.route('/<project_name>/details-setup', methods=['GET', 'POST'])
# @p.route('/new', methods=['GET', 'POST'])
# def project_setup(project_name = None):
#     conn = setup.get_db()   
#     data = {}

#     if project_name: # Edit case loads existing project data
#         project = projects.list_project_details(conn, project_name)[0]

#         if project:
#             # Populate data from the database
#             data['button'] = 'Update'
#             data['project_name'] = project_name
#             data['start_date'] = project[1]
#             data['end_date'] = project[2] or ''
#             data['progress'] = project[-1] or ''
#             data['button'] = 'Update'

#     else:
#         data['button'] = 'Create'

#     # Override data with session data
#     data['error'] = session.pop('error', '')
#     data['project_name'] = session.pop('project_name', data.get('project_name', ''))
#     data['start_date'] = session.pop('start_date', data.get('start_date', ''))
#     data['end_date'] = session.pop('end_date', data.get('end_date', ''))
#     data['progress'] = int(session.pop('progress', data.get('progress', 1) or 1))

#     if request.method == 'POST':
           
#         action = request.form['button'].lower()
        
#         # Collect form data
#         form_project_name = session['project_name'] = request.form['project-name']
#         form_start_date = session['start_date'] = request.form['start-date']
#         form_end_date = session['end_date'] = request.form.get('end-date', '')
#         form_progress = session['progress'] = int(request.form.get('progress', 1) or 1)

#         # Validation check for required fields
#         if not form_project_name or not form_start_date:
#             session['error'] = 'Please input relevant details!'
#             return redirect(url_for('projects.project_setup', project_name=project_name))

#         # Data validation
#         val_start_date = datetime.strptime(form_start_date, "%Y-%m-%d").date()

#         if form_end_date:
#             val_end_date = datetime.strptime(form_end_date, "%Y-%m-%d").date()
#         else:
#             val_end_date = date.today()

#         if val_start_date > date.today() or val_end_date < val_start_date:
#             session['error'] = f'Please input valid start and/or end dates!'
#             return redirect(url_for('projects.project_setup', project_name=project_name))
        
#         if (form_end_date and form_progress < 100) or (form_progress == 100 and not form_end_date):
#             session['error'] = f'Please update completion information.'
#             return redirect(url_for('projects.project_setup', project_name=project_name))


#         if action == 'create':
#             # Validation check whether project exists already
#             if projects.list_project_details(conn, form_project_name):
#                 session['error'] = 'Project already exists!'
#                 return redirect(url_for('projects.project_setup'))
            
#             # Else creates project
#             else:
#                 projects.create_project(conn, form_project_name, form_start_date, form_end_date, form_progress)

#                 session.clear()
#                 return redirect(url_for('projects.floss_setup', project_name=form_project_name))

#         elif action == 'update':
#             # Updates project details
#             projects.update_project(conn, form_project_name, form_end_date)
#             projects.update_project_progress(conn, form_project_name, form_progress)

#             session.clear()
#             return redirect(url_for('projects.floss_setup', project_name=form_project_name))

#     return render_template('project_setup.html', data=data)

# # Project floss page
# @p.route('/<project_name>/floss-setup', methods=['GET', 'POST'])
# def floss_setup(project_name):
#     conn = setup.get_db()

#     floss_list = session.pop('floss_list', []) # Gets floss_list in session

#     # If not a list/tuple, try fetching from DB
#     if not floss_list:
#         floss_list = projects.list_project_floss(conn, project_name)
    
#     # If still not a list/tuple, force empty list
#     if not floss_list:
#         floss_list = []
    

        
#         # Add more floss fields
#         if action == 'add-floss':
#             floss_items = request.form.getlist('floss-item')
#             floss_list = [tuple(item.strip().split()) for item in floss_items]

#             floss_list.append((' ', ' '))

#             session['floss_list'] = floss_list

#             return redirect(url_for('projects.floss_setup', project_name=project_name))

#         # Submit final data
#         if action == 'submit-floss':

#             # Retrieve all from 'floss-item' input fields
#             floss_items = request.form.getlist('floss-item')

#             # Deletes current floss in project_details
#             projects.project_del_all_floss(conn, project_name)

#             for f in floss_items:
#                 f = f.strip() # Floss added by user will have whitespace
#                 brand, fno = floss.fix_floss_input(f)

#                 if brand and fno:
#                     projects.project_add_floss(conn, project_name, brand, fno)

#             return redirect(url_for('projects.project_page', project_name=project_name))
        
#     return render_template('floss_setup.html', floss_list=floss_list, project_name=project_name)