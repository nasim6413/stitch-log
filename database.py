import sqlite3
import pandas as pd
import re

class Database:
    def __init__(self):
        self.brands = ['DMC', 'Anchor']

        conn = sqlite3.connect('floss.db')
        cursor = conn.cursor()
                
        # Checks whether database is empty
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        # If database empty, performs setup
        if not tables:
            self.set_up(cursor)
            
        conn.commit()
        cursor.close()
        conn.close()
        
    def set_up(self, cursor):        
        # Creating tables if it doesn't already exist
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
        
        # Opens CSVs and drops rows with no conversions
        dmc_to_anchor = pd.read_csv('database/dmc_to_anchor.csv', names=['dmc', 'anchor', 'hex', 'colour'])
        dmc_to_anchor = dmc_to_anchor[dmc_to_anchor.anchor != 'NA']
               
        anchor_to_dmc = pd.read_csv('database/anchor_to_dmc.csv', names=['anchor', 'dmc', 'hex', 'colour'])
        anchor_to_dmc = anchor_to_dmc[anchor_to_dmc.dmc != 'NA']
        
        # Populate conversion tables
        dmc_to_anchor.to_sql('dmc_to_anchor', self.conn, if_exists='append', index = False)
        anchor_to_dmc.to_sql('anchor_to_dmc', self.conn, if_exists='append', index = False)
        
        # Creates stock table
        cursor.execute("""
            CREATE TABLE stock (
                brand TEXT NOT NULL,
                fno TEXT NOT NULL
            );
        """)
    
    def connect(self):
        try:
            conn = sqlite3.connect('floss.db')
            return conn
        except:
            return False
        
    # Fixes input
    def re_input(self, item):
        pattern = r'(DMC|Anchor)\s*(\w?\d{1,4}|B5200|ECRU|White)'
        match = re.match(pattern, item, re.IGNORECASE)
        
        brand = match.group(1)
        fno = match.group(2)
        
        if brand.upper() == self.brands[0]:
            brand = brand.upper() 
            
        if brand.capitalize() == self.brands[1]:
            brand = brand.capitalize()
        
        if fno.capitalize() == 'White' or fno.capitalize() == 'Ecru':
            fno = fno.capitalize()
            
        # Fixes pattern numbers that include letter
        fno_pattern = r'(.)(\d{1,4})'
        fno_match = re.match(fno_pattern, fno, re.IGNORECASE)

        if fno_match:
            fno = fno_match.group(1).upper() + fno_match.group(2)
        
        return brand, fno
        
    # Returns list of current stock
    def flist(self, conn):
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

    # Returns count of items in stock
    def stock_count(self, conn):
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT * FROM stock
                       """)
        
        stock_no = len(cursor.fetchall())

        cursor.close()
        return stock_no

    # Returns info for specified floss number
    def search(self, conn, brand, fno):
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
        
    # Returns possible conversion for specified floss number
    def gen_convert(self, conn, brand, fno):
        cursor = conn.cursor()

        if brand == self.brands[0]:
            cursor.execute("""
                        SELECT dmc, anchor, hex
                        FROM dmc_to_anchor
                        WHERE dmc_to_anchor.dmc = ?;
                        """,
                        (fno,))
            
        if brand == self.brands[1]:
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
            
    # Returns possible conversions for specified floss number according to what is available in stock        
    def stock_convert(self, conn, brand, fno):
        cursor = conn.cursor()

        if brand == self.brands[0]:
            cursor.execute("""
                           SELECT DISTINCT dmc_to_anchor.dmc, stock.fno AS anchor, dmc_to_anchor.hex
                           FROM stock 
                                INNER JOIN dmc_to_anchor 
                                ON (dmc_to_anchor.anchor = stock.fno)
                           WHERE dmc_to_anchor.dmc = ?;
                           """,
                           (fno,))
            
        if brand == self.brands[1]:
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
        
    # Adds to stock
    def add(self, conn, brand, fno):
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
        
    # Deletes from stock
    def delete(self, conn, brand, fno):
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