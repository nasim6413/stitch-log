import datetime
from ..utils.utils import natural_key

# LIST PROJECTS
def list_all_projects(conn):

    """Returns list of all projects with details."""

    cursor = conn.cursor()
    
    try:
        cursor.execute("""
                SELECT project_name
                FROM project_details;
                """)
        
        output = cursor.fetchall()
        cursor.close()
        return output
    
    except:
        cursor.close()
        return False


def list_project_details(conn, project_name):
    
    """Returns specified project with start dates and progress."""
    
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT *
            FROM project_details
            WHERE project_name = ?;
            """,
            (project_name,))
    
        output = cursor.fetchall()
        cursor.close()
        return output

    except:
        cursor.close()
        return False

# PROJECT CREATION / UPDATING
def create_project(conn):
    
    """Creates new cross-stitch project."""

    cursor = conn.cursor()

    # Returns most recent untitled project
    cursor.execute("""
                    SELECT project_name
                    FROM project_details
                    WHERE project_name LIKE 'Untitled-%'
                    ORDER BY CAST(SUBSTR(project_name, 10) AS INTEGER) DESC
                    LIMIT 1;
                   """)
    
    try:
        output = cursor.fetchone()
        if not output:
            project_name = 'Untitled-00'
        
        else:
            project_num = output[0].split('-')[1]
            project_name = f'Untitled-{int(project_num) + 1:02d}'

        start_date = datetime.datetime.now()
        end_date = None

        cursor.execute("""
                       INSERT INTO project_details (project_name, start_date, end_date)
                       VALUES (?, ?, ?);
                       """,
                       (project_name, start_date, end_date))
        
        conn.commit()
        cursor.close()
        return project_name
    
    except:
        cursor.close()
        return False
    
def delete_project(conn, name):
    
    """Deletes project and relevant data."""
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
                       DELETE FROM project_details
                       WHERE project_name = ?
                       ;
                       """,
                       (name,))
        
        conn.commit()
        cursor.close()
        return True 
    
    except:
        cursor.close()
        return False 

# PROJECT UPDATES
def update_project_name(conn, project_id, new_name):
    
    """Updates project name."""
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
                       UPDATE project_details
                       SET project_name = ?
                       WHERE id = ?;
                       """,
                       (new_name, project_id,))
        
        conn.commit()
        cursor.close()
        return True
    
    except:
        cursor.close()
        return False
    
# def update_project(conn, name, end_date):
    
#     """Updates project's end date."""
    
#     cursor = conn.cursor()
    
#     if search_project(conn, name):
#         cursor.execute("""UPDATE project_details
#                        SET end_date = ?
#                        WHERE project_name = ?;
#                        """,
#                        (end_date, name))
        
#         conn.commit()
#         cursor.close()
#         return True
    
#     else:
#         return False
    
# def update_project_progress(conn, name, progress):
    
#     """Updates project's progress."""
    
#     cursor = conn.cursor()
    
#     if search_project(conn, name):
#         cursor.execute("""UPDATE project_details
#                        SET progress = ?
#                        WHERE project_name = ?;
#                        """,
#                        (progress, name))
        
#         conn.commit()
#         cursor.close()
#         return True
    
#     else:
#         return False

# PROJECT FLOSS
def list_project_floss(conn, project_name):
    
    """Returns given project's floss details and whether floss is in stock."""
    
    cursor = conn.cursor()

    try:
        cursor.execute("""SELECT project_floss.brand, project_floss.fno, (stock.id IS NOT NULL) AS available
                        FROM project_floss
                        LEFT JOIN stock ON project_floss.brand = stock.brand AND project_floss.fno = stock.fno
                        WHERE project_floss.project_name = ?
                        ORDER BY project_floss.brand;
                        """,
                        (project_name,))
    
        output = cursor.fetchall()
        output = sorted(output, key=lambda row: (row[0].lower(), natural_key(row[1])))
        
        cursor.close()
        return output

    except:
        cursor.close()
        return False

def project_add_floss(conn, name, brand, fno):
    
    """Adds floss to project list."""
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
                       INSERT INTO project_floss (project_name, brand, fno)
                       VALUES (?, ?, ?);
                       """,
                       (name, brand, fno))
        conn.commit()
        cursor.close()
        return True
    
    except:
        cursor.close()
        return False

def project_delete_floss(conn, name, brand, fno):
    
    """Deletes floss from project list."""
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
                       DELETE FROM project_floss
                       WHERE project_name = ? AND brand = ? AND fno = ?;
                       """, 
                       (name, brand, fno))
        
        conn.commit()
        cursor.close()
        return True
    
    except:
        cursor.close()
        return False

def project_del_all_floss(conn, name):
    
    """Delete all floss associated with project."""

    cursor = conn.cursor()

    try:
        cursor.execute("""
                DELETE FROM project_floss
                WHERE project_name = ?
                ;
                """,
                (name,))

        conn.commit()
        cursor.close()
        return True

    except:
        cursor.close()
        return False