import sqlite3
import re

BRANDS = ['DMC', 'Anchor']

# Fixes user input
def re_input(match):
    comm = match.group(1)
    comm = comm.lower()
    
    brand = match.group(2)
    fno = match.group(3)
    
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
    
    return comm, brand, fno

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("floss.db")
        
        cursor = self.conn.cursor()
        
        # Create table if it doesn't already exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dmc_to_anchor (
            dmc TEXT NOT NULL PRIMARY KEY,
            anchor TEXT NOT NULL,
            hex TEXT,
            fname TEXT
        );
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock (
                brand TEXT NOT NULL,
                fno TEXT NOT NULL
            );
        """)

        self.conn.commit()
        cursor.close()
    
    def disconnect(self):
        self.conn.close()
        return
        
    # Returns list of current stock
    def flist(self):
        cursor = self.conn.cursor()
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

    # Returns count of items in stock
    def stock_count(self):
        cursor = self.conn.cursor()
        cursor.execute("""
                       SELECT * FROM stock
                       """)
        
        stock_no = len(cursor.fetchall())

        cursor.close()
        return stock_no

    # Returns info for specified floss number
    def search(self, brand, fno):
        cursor = self.conn.cursor()

        #NOTE: Does not support Anchor
        if brand == BRANDS[0]:            
            cursor.execute("""
                           SELECT stock.*
                           FROM stock 
                           WHERE stock.fno = ?
                           """, 
                           (fno,))

        try:
            output = cursor.fetchone()
            if output:
                cursor.close()
                return True
            else: # Empty output
                return False
            
        except:
            return False
        
    # Returns possible conversions for specified floss number according to what is available in stock        
    def convert_stock(self, brand, fno):
        cursor = self.conn.cursor()

        if brand == BRANDS[0]:
            cursor.execute("""
                           SELECT DISTINCT dmc_to_anchor.dmc, stock.fno AS anchor, dmc_to_anchor.hex
                           FROM stock 
                                INNER JOIN dmc_to_anchor 
                                ON (dmc_to_anchor.anchor = stock.fno)
                           WHERE dmc_to_anchor.dmc = ?;
                           """,
                           (fno,))
        
        try:
            output = cursor.fetchall()
            cursor.close()
            return output
                
        except:
            cursor.close()
            return False
    
    # Returns possible conversion for specified floss number
    def convert(self, brand, fno):
        cursor = self.conn.cursor()

        if brand == BRANDS[0]:
            cursor.execute("""
                        SELECT dmc, anchor, hex
                        FROM dmc_to_anchor
                        WHERE dmc_to_anchor.dmc = ?;
                        """,
                        (fno,))
            
            try:
                output = cursor.fetchall()
                cursor.close()
                return output

            except:
                cursor.close()
                return False
        
    # Adds to stock
    def add(self, brand, fno):
        cursor = self.conn.cursor()

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
            self.conn.commit()

            cursor.close()
            return True
        
    # Deletes from stock
    def delete(self, brand, fno):
        cursor = self.conn.cursor()

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
            self.conn.commit()
            
            cursor.close()
            return True   
        
        else: 
            cursor.close()
            return False  