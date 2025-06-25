from ..utils import *

def search_project(conn, name):
    
    """Checks whether project exists."""
    
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM project_details
                   WHERE project_name = ?;
                   """,
                   (name,))
    
    output = cursor.fetchall()
    cursor.close()
    
    if len(output) > 0:
        return True
    
    else:
        return False
    
def search_project_floss(conn, name, brand, fno):
    
    """Check whether a floss is listed under a project."""
    
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT project_name, brand, fno FROM project_floss
                   WHERE project_name = ? AND brand = ? AND fno = ?;
                   """,
                   (name, brand, fno))
    
    output = cursor.fetchall()
    cursor.close()
    
    if len(output) > 0:
        return True
    else:
        return False

def create_project(conn, name, start_date):
    
    """Creates new cross-stitch project (if not existing)."""
    
    cursor = conn.cursor()
    
    if search_project(conn, name):
        
        cursor.close()
        return False
    
    else:
        cursor.execute("""
                       INSERT INTO project_details (project_name, start_date)
                       VALUES (?, ?);
                       """,
                       (name, start_date))
        
        conn.commit()
        cursor.close()
        return True  
    
def delete_project(conn, name):
    
    """Deletes project and relevant data."""
    
    cursor = conn.cursor()
    
    if search_project(conn, name):
        cursor.execute("""
                       DELETE FROM project_details
                       WHERE project_name = ?
                       ;
                       """,
                       (name,))
        
        conn.commit()
        cursor.close()
        return True 
    
    else:
        return False 
    
def update_project(conn, name, end_date):
    
    """Updates project's end date.""" #TODO: add more functionality to this
    
    cursor = conn.cursor()
    
    if search_project(conn, name):
        cursor.execute("""UPDATE project_details
                       SET end_date = ?
                       WHERE project_name = ?;
                       """,
                       (end_date, name))
        
        conn.commit()
        cursor.close()
        return True
    
    else:
        return False

def project_add_floss(conn, name, brand, fno):
    
    """Adds floss to project list."""
    
    cursor = conn.cursor()
    
    # Checks that project exists and floss is not listed under it
    if search_project(conn, name) and not search_project_floss(conn, name,brand, fno):
        cursor.execute("""
                       INSERT INTO project_floss (project_name, brand, fno)
                       VALUES (?, ?, ?);
                       """,
                       (name, brand, fno))
        conn.commit()
        cursor.close()
        return True
    
    else:
        return False

def project_del_floss(conn, name, brand, fno):
    
    """Deletes floss from project list."""
    
    cursor = conn.cursor()
    
    # Checks that project exists and floss is listed under it
    if search_project(conn, name, brand, fno):
        cursor.execute("""
                       DELETE FROM project_floss
                       WHERE project_name = ? AND brand = ? AND fno = ?;
                       """, 
                       (name, brand, fno))
        
        conn.commit()
        cursor.close()
        return True
    
    else:
        return False

def project_del_all_floss(conn, name):
    
    """Delete all floss associated with project."""

    cursor = conn.cursor()

    if search_project(conn, name):
        cursor.execute("""
                DELETE FROM project_floss
                WHERE project_name = ?
                ;
                """,
                (name,))

        conn.commit()
        cursor.close()
        return True

    else:
        return False

    
def list_projects(conn):
    
    """Returns list of all projects with start and end dates."""
    
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT project_name, start_date, end_date
                   FROM project_details;
                   """)
    
    try:
        output = cursor.fetchall()
        cursor.close()
        return output

    except:
        cursor.close()
        return False


def list_project_details(conn, name):
    
    """Returns given project's floss details and whether floss is in stock."""
    
    cursor = conn.cursor()
    if search_project(conn, name):
        cursor.execute("""SELECT project_floss.brand, project_floss.fno, (stock.id IS NOT NULL) AS available
                       FROM project_floss
                       LEFT JOIN stock ON project_floss.brand = stock.brand AND project_floss.fno = stock.fno
                       WHERE project_floss.project_name = ?
                       ORDER BY project_floss.brand;
                       """,
                       (name,))
        
        output = cursor.fetchall()
        output = sorted(output, key=lambda row: (row[0].lower(), natural_key(row[1])))
        
        cursor.close()
        return output
    
    else:
        return False