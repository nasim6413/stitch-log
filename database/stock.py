def stock_list(conn):
    
    """Returns list of current stock."""
    
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT * FROM stock
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

    try:
        output = cursor.fetchone()
        if output:
            cursor.close()
            return output
        else: # Empty output
            return False
        
    except:
        return False
    
def stock_add(conn, brand, fno):
    
    """Adds specified floss to stock table if not existing."""
    
    cursor = conn.cursor()

    cursor.execute("""
                    SELECT * FROM stock 
                    WHERE stock.brand = ? AND stock.fno = ?;
                    """, 
                    (brand, fno,))
    
    if cursor.fetchone():
        cursor.close()
        return False

    else:
        cursor.execute("""
                        INSERT INTO stock (brand, fno)
                        VALUES (?, ?);
                        """,
                        (brand, fno))
        
        conn.commit()
        cursor.close()
        return True
    
def stock_del(conn, brand, fno):

    """Deletes specified floss from stock table if existing."""
    
    cursor = conn.cursor()

    cursor.execute("""
                    SELECT * FROM stock 
                    WHERE stock.brand = ? AND stock.fno = ?;
                    """, 
                    (brand, fno,))
    
    if cursor.fetchone():
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