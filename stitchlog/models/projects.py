from ..utils import *

def create_project(conn, name, start_date, end_date = False, progress = 1):
    
    """Creates new cross-stitch project (if not existing)."""
    
    cursor = conn.cursor()
    
    if search_project(conn, name):
        
        cursor.close()
        return False
    
    else:
        cursor.execute("""
                       INSERT INTO project_details (project_name, start_date, end_date, progress)
                       VALUES (?, ?,  ?, ?);
                       """,
                       (name, start_date, end_date, progress))
        
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

def list_project_details(conn, project_name = False):
    
    """Returns list of all projects with start dates and progress."""
    
    cursor = conn.cursor()

    # Default returns all project details
    if not project_name:
        cursor.execute("""
                    SELECT project_name, progress
                    FROM project_details
                    ORDER BY progress;
                    """)
    
    # Else returns specific project details
    elif project_name:
        cursor.execute("""
            SELECT *
            FROM project_details
            WHERE project_name = ?;
            """,
            (project_name,))
    
    try:
        output = cursor.fetchall()
        cursor.close()
        return output

    except:
        cursor.close()
        return False
    
def update_project(conn, name, end_date):
    
    """Updates project's end date."""
    
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
    
def update_project_progress(conn, name, progress):
    
    """Updates project's progress."""
    
    cursor = conn.cursor()
    
    if search_project(conn, name):
        cursor.execute("""UPDATE project_details
                       SET progress = ?
                       WHERE project_name = ?;
                       """,
                       (progress, name))
        
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
    
def list_project_floss(conn, name):
    
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