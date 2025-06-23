import re
BRANDS = ['DMC', 'Anchor']
FLOSS_PATTERN = r'(DMC|Anchor)\s*(\w?\d{1,4}|B5200|ECRU|White)'

def natural_key(s):
    """Natural sorting for floss lists."""
    s = str(s)
    parts = []
    
    for t in re.split('(\d+)', s):
        if t.isdigit():
            parts.append(int(t))
        else:
            parts.append(t.lower())
    return parts

def search_stock(conn, brand, fno):

    """Checks whether specified floss exists in stock."""
    
    cursor = conn.cursor()
        
    cursor.execute("""
                    SELECT stock.*
                    FROM stock 
                    WHERE stock.brand = ? AND stock.fno = ?
                    """, 
                    (brand, fno,))

    output = cursor.fetchall()
    if len(output) > 0:
        cursor.close()
        return True
        
    else:
        return False

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