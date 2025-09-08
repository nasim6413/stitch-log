from flask import Blueprint, render_template, request
from stitchlog.models import setup, projects, extractor, floss
from ..models.search import search_project, search_project_floss
from ..utils.responses import *

p = Blueprint('projects', __name__, url_prefix='/projects')

@p.route('/')
def projects_home():   
    return render_template('projects.html')

@p.route('/<project_name>')
def project_page(project_name):
    return render_template('project/project.html', project_name=project_name)

@p.route("/list", methods=["GET"])
def projects_list():
    """Retrieve and return a list of all projects with progress details."""
    conn = setup.get_db()
    rows = projects.list_all_projects(conn)

    if not rows:
        return error_response("Error in retrieving projects list.")

    project_list = [
        {
            "project_name": row[0],
            "project_progress": row[1],
        }
        for row in rows
    ]
    return success_response(project_list)

@p.route("/<project_name>/details", methods=["GET"])
def project_page_details(project_name):
    """Retrieve specific project details by name."""
    conn = setup.get_db()

    if not search_project(conn, project_name):
        return error_response("Project does not exist!")

    details = projects.list_project_details(conn, project_name)
    if not details:
        return error_response("There was a problem retrieving the project details.")

    return success_response(details)

@p.route("/create", methods=["GET", "POST"])
def project_creation():
    """Create a new project and return its name."""
    conn = setup.get_db()
    result = projects.create_project(conn)

    if not result:
        return error_response("Error creating project.")

    return success_response({"project_name": result})
 
# TODO:Project amend details
    
@p.route("/<project_name>/delete", methods=["POST"])
def project_delete(project_name):
    """Delete a project and all associated floss."""
    conn = setup.get_db()

    if not search_project(conn, project_name):
        return error_response("Project does not exist!")

    result_project = projects.delete_project(conn, project_name)
    result_floss = projects.project_del_all_floss(conn, project_name)

    if not (result_project and result_floss):
        return error_response("Error deleting project!")

    return success_response()
        
@p.route("/<project_name>/floss/list", methods=["GET"])
def project_page_floss(project_name):
    """List all floss associated with a project."""
    conn = setup.get_db()

    if not search_project(conn, project_name):
        return error_response("Project does not exist!")

    rows = projects.list_project_floss(conn, project_name)
    if not rows:
        return error_response("No floss associated with project.")

    floss_list = [
        {
            "brand": row[0],
            "fno": row[1],
            "availability": row[2],
        }
        for row in rows
    ]
    return success_response(floss_list)
    
@p.route("/<project_name>/floss/add", methods=["POST"])
def project_add_floss(project_name):
    """Add a floss item to a project."""
    conn = setup.get_db()
    data = request.get_json()
    item = data.get("floss", "").strip()

    brand, fno = floss.fix_floss_input(item)

    if search_project_floss(conn, project_name, brand, fno):
        return error_response("Floss already in project.")

    result = projects.project_add_floss(conn, project_name, brand, fno)
    if not result:
        return error_response("Error adding floss to project.")

    return success_response()

@p.route("/<project_name>/floss/delete", methods=["POST"])
def project_del_floss(project_name):
    """Delete a floss item from a project."""
    conn = setup.get_db()
    data = request.get_json()
    item = data.get("floss", "").strip()

    brand, fno = floss.fix_floss_input(item)

    if not search_project_floss(conn, project_name, brand, fno):
        return error_response("Floss not in project.")

    result = projects.project_delete_floss(conn, project_name, brand, fno)
    if not result:
        return error_response("Error deleting floss from project.")

    return success_response()
    
@p.route("/<project_name>/floss/extract", methods=["GET", "POST"])
def project_floss_extractor(project_name):
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