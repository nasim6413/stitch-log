import datetime
from ..utils.utils import natural_key

# LIST PROJECTS
def list_all_projects(conn):

    """Returns list of all projects with details."""

    cursor = conn.cursor()
    
    try:
        cursor.execute("""
                SELECT project_id, name
                FROM projects;
                """)
        #TODO: add details
        
        output = cursor.fetchall()
        cursor.close()
        return output
    
    except:
        cursor.close()
        return False


def project_details(conn, project_id):
    
    """Returns project with full details."""
    
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT *
            FROM projects
            WHERE project_id = ?;
            """,
            (project_id,))
    
        output = cursor.fetchone()
        print(output)
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
                    SELECT name
                    FROM projects
                    WHERE name LIKE 'Untitled-%'
                    ORDER BY CAST(SUBSTR(name, 10) AS INTEGER) DESC
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
                       INSERT INTO projects (name, start_date, end_date)
                       VALUES (?, ?, ?);
                       """,
                       (project_name, start_date, end_date))
        
        project_id = cursor.lastrowid

        data = {
            "project_id" : project_id,
            "project_name" : project_name
        }
        
        conn.commit()
        cursor.close()
        return data
    
    except:
        cursor.close()
        return False
    
def delete_project(conn, project_id):
    
    """Deletes project and relevant data."""
    
    cursor = conn.cursor()
    
    try:
        # Deletes project details
        cursor.execute("""
                       DELETE FROM projects
                       WHERE project_id = ?
                       ;
                       """,
                       (project_id,))

        # Deletes project floss
        cursor.execute("""
            DELETE FROM project_floss
            WHERE project_id = ?
            ;
            """,
            (project_id,))

        conn.commit()
        cursor.close()
        return True 
    
    except:
        cursor.close()
        return False 

# PROJECT UPDATES
def update_project(conn, data):
    
    """Updates project details."""
    
    cursor = conn.cursor()
    
    try:
        # Update project name
        cursor.execute("""
                       UPDATE projects
                       SET name = ?, start_date = ?, end_date = ?
                       WHERE project_id = ?;
                       """,
                       (data['project_name'], 
                        data['project_start_date'],
                        data['project_end_date'],
                        data['project_id'],))
        
        # Retrieve list of current project floss
        cursor.execute("""
                       SELECT 
                            brand, 
                            f_no
                        FROM project_floss
                        WHERE project_id = ?;
                       """,
                       (data['project_id'],))
        
        floss_db = cursor.fetchall()
        floss_db = set((row[0], row[1]) for row in floss_db)
        floss_new = set((item["brand"], item["floss"]) for item in data["floss"])

        to_add = floss_new - floss_db   # in new but not in db
        to_delete = floss_db - floss_new   # in db but not in new

        print("Calculating floss to add and delete.")

        for brand, f_no in to_add:
            cursor.execute("""
                        INSERT INTO project_floss (project_id, brand, f_no) 
                        VALUES (?, ?, ?)""",
                        (data["project_id"], brand, f_no)
                        )
            
        for brand, f_no in to_delete:
            cursor.execute("""
                        DELETE FROM project_floss
                        WHERE project_id = ? AND brand = ? AND f_no = ?
                        """,
                        (data["project_id"], brand, f_no)
                        )
                
        conn.commit()
        cursor.close()
        return True
    
    except:
        cursor.close()
        return False

# PROJECT FLOSS
def list_project_floss(conn, project_id):
    
    """Returns given project's floss details and whether floss is in stock."""
    
    cursor = conn.cursor()

    try:
        cursor.execute("""SELECT 
                            project_floss.brand, 
                            project_floss.f_no, 
                            (stock.stock_id IS NOT NULL) AS available
                        FROM project_floss
                        LEFT JOIN stock 
                            ON project_floss.brand = stock.brand 
                            AND project_floss.f_no = stock.f_no
                        WHERE project_floss.project_id = ?
                        ORDER BY project_floss.brand;
                        """,
                        (project_id,))
    
        output = cursor.fetchall()
        output = sorted(output, key=lambda row: (row[0].lower(), natural_key(row[1])))
        
        cursor.close()
        return output

    except:
        cursor.close()
        return False