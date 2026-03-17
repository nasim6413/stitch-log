from flask import Blueprint, render_template, request
from stitchlog.models import setup, projects, extractor, floss
# from ..models.search import search_project
from ..utils.responses import *

p = Blueprint('projects', __name__, url_prefix='/projects')

@p.route('/')
def projects_home():   
    return render_template('project-list.html')

@p.route('/list', methods=['GET'])
def projects_list():
    """Retrieve and return a list of all projects with progress details."""
    conn = setup.get_db()
    rows = projects.list_all_projects(conn)

    if not rows:
        return error_response("Error in retrieving projects list.")

    project_list = [
        {
            "project_id": row[0],
            "project_name": row[1]
        }
        for row in rows
    ]

    return success_response(project_list)

@p.route('/<project_id>')
def project_page(project_id):
    conn = setup.get_db()

    details = projects.project_details(conn, project_id)

    if not details:
        return error_response("There was a problem retrieving the project details.")

    return render_template('project-page.html', project_id=project_id, project_details=details)

@p.route('/<project_id>/floss/list', methods=['GET'])
def project_page_floss(project_id):
    """List all floss associated with a project."""
    conn = setup.get_db()

    rows = projects.list_project_floss(conn, project_id)
    if not rows:
        return error_response("No floss associated with project.")

    floss_list = [
        {
            "brand": row[0],
            "floss": row[1],
            "availability": row[2],
        }
        for row in rows
    ]
    return success_response(floss_list)

@p.route('/create', methods=['GET', 'POST'])
def project_creation():
    """Create a new project and return its name."""
    conn = setup.get_db()
    result = projects.create_project(conn)

    if not result:
        return error_response("Error creating project.")

    return success_response({"project_id": result["project_id"],
                             "project_name": result["project_name"]})

@p.route('/<project_id>/amend')
def amend_project(project_id):
    conn = setup.get_db()

    result = projects.project_details(conn, project_id)
    if not result:
         return error_response("There was a problem retrieving the project details.")

    return render_template('project-amend.html', project_id=project_id, project_details=result)

@p.route('/<project_id>/amend/save', methods=['GET', 'POST'])
def save_changes_project(project_id):
    """Save all changes to project details."""
    conn = setup.get_db()
    data = request.get_json()
    
    # Clean floss inputs
    data["floss"] = [
        {"brand": item["brand"], 
         "floss": floss.fix_floss_input(item["floss"])}
        for item in data["floss"]
    ]
    
    result = projects.update_project(conn, data)
    
    if not result:
        return error_response()
    
    return success_response()

@p.route('/<project_id>/delete', methods=['POST'])
def project_delete(project_id):
    """Delete a project and all associated floss."""
    conn = setup.get_db()

    result_project = projects.delete_project(conn, project_id)

    if not result_project:
        return error_response("Error deleting project!")

    return success_response()
    
@p.route('/<project_id>/floss/extract', methods=['GET', 'POST'])
def project_floss_extractor(project_id):
    """Extract floss list from an uploaded PDF."""
    if "file" not in request.files:
        return error_response("No file uploaded.")

    pattern_file = request.files["file"]
    if not extractor.validate_upload(pattern_file):
        return error_response("Invalid file input!")

    extracted_floss = extractor.extract_floss(pattern_file)
    if not extracted_floss:
        return error_response("Error extracting floss.")

    return success_response(extracted_floss)