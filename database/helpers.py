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