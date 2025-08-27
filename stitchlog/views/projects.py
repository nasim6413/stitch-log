from flask import Blueprint, render_template, request
from stitchlog.models import setup, projects, extractor, floss
from datetime import datetime, date
from ..models.search import search_project, search_project_floss
from ..utils.responses import *

p = Blueprint('projects', __name__, url_prefix='/projects')

@p.route('/')
def projects_home():   
    return render_template('projects_page.html')

@p.route('/<project_name>')
def project_page(project_name):
    return render_template('project_details.html', project_name=project_name)

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
    ]) if rows else error_response("Error in retrieving projects list.")

# Project page
@p.route('/<project_name>/details', methods=['GET'])
def project_page_details(project_name):
    conn = setup.get_db()
    
    if search_project(conn, project_name):
        details = projects.list_project_details(conn, project_name)

        return success_response(details) if details else error_response("There a problem in retrieving the project details.")
    
    else:
        return error_response("Project does not exist!")

# Project creation
@p.route('/create', methods=['GET', 'POST'])
def project_creation():
    conn = setup.get_db()
    result = projects.create_project(conn)

    return success_response({"project_name" : result}) if result else error_response("Error in creating project.")
 
# TODO:Project amend details
            
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
        
@p.route('/<project_name>/floss/list', methods=['GET'])
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
    
# Project retrieve floss from PDF
@p.route('/<project_name>/floss/extract', methods=['GET', 'POST'])
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