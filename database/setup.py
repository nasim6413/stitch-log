import pandas as pd
import re
       
BRANDS = ['DMC', 'Anchor']

def set_up(conn):   
    
    """Performs first-time setup for database."""
    
    cursor = conn.cursor()
         
    # Conversion tables
    cursor.execute("""
        CREATE TABLE dmc_to_anchor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dmc TEXT NOT NULL,
        anchor TEXT NOT NULL,
        hex TEXT,
        colour TEXT
        );
    """)
    
    cursor.execute("""
        CREATE TABLE anchor_to_dmc (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        anchor TEXT NOT NULL,
        dmc TEXT NOT NULL,
        hex TEXT,
        colour TEXT
        );
    """)
    
    # Retrieving conversion data
    dmc_to_anchor = pd.read_csv('./conversions/dmc_to_anchor.csv', names=['dmc', 'anchor', 'hex', 'colour'])
    dmc_to_anchor = dmc_to_anchor[dmc_to_anchor.anchor != 'NA']
            
    anchor_to_dmc = pd.read_csv('./conversions/anchor_to_dmc.csv', names=['anchor', 'dmc', 'hex', 'colour'])
    anchor_to_dmc = anchor_to_dmc[anchor_to_dmc.dmc != 'NA']
    
    # Populate conversion tables
    dmc_to_anchor.to_sql('dmc_to_anchor', conn, if_exists='append', index = False)
    anchor_to_dmc.to_sql('anchor_to_dmc', conn, if_exists='append', index = False)
    
    # Stock table
    cursor.execute("""
        CREATE TABLE stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            fno TEXT NOT NULL
        );
    """)
    
    # Projects table
    cursor.execute("""
        CREATE TABLE project_details (
            project_name TEXT NOT NULL PRIMARY KEY,
            start_date TIMESTAMP NOT NULL,
            end_date TIMESTAMP
        );
    """)
    
    # Project floss table
    cursor.execute("""
        CREATE TABLE project_floss (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            brand TEXT NOT NULL,
            fno TEXT NOT NULL
        );
    """)

def re_input(item):
    
    """Fixes input."""
    
    pattern = r'(DMC|Anchor)\s*(\w?\d{1,4}|B5200|ECRU|White)'
    match = re.match(pattern, item, re.IGNORECASE)
    
    brand = match.group(1)
    fno = match.group(2)
    
    if brand.upper() == BRANDS[0]:
        brand = brand.upper() 
        
    if brand.capitalize() == BRANDS[1]:
        brand = brand.capitalize()
    
    if fno.capitalize() == 'White' or fno.capitalize() == 'Ecru':
        fno = fno.capitalize()
        
    # Fixes pattern numbers that include letter
    fno_pattern = r'(.)(\d{1,4})'
    fno_match = re.match(fno_pattern, fno, re.IGNORECASE)

    if fno_match:
        fno = fno_match.group(1).upper() + fno_match.group(2)
    
    return brand, fno
    
def gen_convert(conn, brand, fno):
    
    """Returns all possible conversions for a specified floss."""
    
    cursor = conn.cursor()

    if brand == BRANDS[0]:
        cursor.execute("""
                    SELECT dmc, anchor, hex
                    FROM dmc_to_anchor
                    WHERE dmc_to_anchor.dmc = ?;
                    """,
                    (fno,))
        
    if brand == BRANDS[1]:
        cursor.execute("""
                    SELECT anchor, dmc, hex
                    FROM anchor_to_dmc
                    WHERE anchor_to_dmc.anchor = ?;
                    """,
                    (fno,))
        
    try:
        output = cursor.fetchall()
        cursor.close()
        return output

    except:
        cursor.close()
        return False
        

def stock_convert(conn, brand, fno):
    
    """Returns possible conversions for a specified floss if available from stock."""
    
    cursor = conn.cursor()

    if brand == BRANDS[0]:
        cursor.execute("""
                        SELECT DISTINCT dmc_to_anchor.dmc, stock.fno AS anchor, dmc_to_anchor.hex
                        FROM stock 
                            INNER JOIN dmc_to_anchor 
                            ON (dmc_to_anchor.anchor = stock.fno)
                        WHERE dmc_to_anchor.dmc = ?;
                        """,
                        (fno,))
        
    if brand == BRANDS[1]:
        cursor.execute("""
                        SELECT DISTINCT anchor_to_dmc.anchor, stock.fno AS anchor, anchor_to_dmc.hex
                        FROM stock 
                            INNER JOIN anchor_to_dmc 
                            ON (anchor_to_dmc.dmc = stock.fno)
                        WHERE anchor_to_dmc.anchor = ?;
                        """,
                        (fno,))
    
    try:
        output = cursor.fetchall()
        cursor.close()
        return output
            
    except:
        cursor.close()
        return False