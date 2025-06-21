def stock_list(conn):
    
    """Returns list of current stock."""
    
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT brand, fno
                    FROM stock
                    ORDER BY brand, fno;
                    """)
    
    try:
        output = cursor.fetchall()
        cursor.close()
        return output

    except:
        cursor.close()
        return False

def stock_count(conn):
    
    """Returns count of current stock."""
        
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT * FROM stock
                    """)
    
    stock_no = len(cursor.fetchall())

    cursor.close()
    return stock_no

def stock_search(conn, brand, fno):

    """Returns rows/s for specified floss."""
    
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

def stock_add(conn, brand, fno):
    
    """Adds specified floss to stock table if not existing."""
    
    cursor = conn.cursor()

    if not stock_search(conn, brand, fno):
        cursor.execute("""
                        INSERT INTO stock (brand, fno)
                        VALUES (?, ?);
                        """,
                        (brand, fno))
        
        conn.commit()
        cursor.close()
        return True
    
    else:
        return False
    
def stock_del(conn, brand, fno):

    """Deletes specified floss from stock table if existing."""
    
    cursor = conn.cursor()

    if stock_search(conn, brand, fno):
        cursor.execute("""
                        DELETE FROM stock
                        WHERE stock.brand = ? AND stock.fno = ?;
                        """,
                        (brand, fno))
        
        conn.commit()
        cursor.close()
        return True   
    
    else: 
        cursor.close()
        return False  