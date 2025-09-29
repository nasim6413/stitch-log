def search_stock(conn, brand, fno):

    """Checks whether specified floss exists in stock."""
    
    cursor = conn.cursor()
        
    cursor.execute("""
                    SELECT stock.*
                    FROM stock 
                    WHERE stock.brand = ? 
                        AND stock.f_no = ?
                    """, 
                    (brand, fno,))

    output = cursor.fetchall()
    if len(output) > 0:
        cursor.close()
        return True
        
    else:
        return False
    

def search_project(conn, name):
    
    """Checks whether project exists and returns project id."""
    
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT project_id 
                   FROM projects
                   WHERE name = ?;
                   """,
                   (name,))
    
    output = cursor.fetchone()
    cursor.close()
    
    if len(output) > 0:
        return output[0]
    
    else:
        return False
    
def search_project_floss(conn, project_id, brand, fno):

    """Check whether a floss is listed under a project."""

    cursor = conn.cursor()
    cursor.execute("""
                   SELECT 
                        project_id, 
                        brand, 
                        f_no 
                    FROM project_floss
                    WHERE project_id = ? 
                        AND brand = ? 
                        AND f_no = ?;
                    """,
                    (project_id, brand, fno))

    output = cursor.fetchall()
    cursor.close()

    if len(output) > 0:
        return True
    else:
        return False