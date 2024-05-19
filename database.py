import psycopg2
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
        
    if fno == 'b5200':
        fno = 'B5200'
    
    return comm, brand, fno

class Database:
    def __init__(self, config):
        self.conn = psycopg2.connect(**config)
    
    def disconnect(self):
        self.conn.close()
        return
        
    # Returns list of current stock
    def flist(self):
        cursor = self.conn.cursor()
        cursor.execute("""
                    SELECT * FROM public.stock
                    ORDER BY fno;
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
                       SELECT * FROM public.stock
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
                           SELECT stock.*, dmc.name, dmc.hex
                           FROM public.stock INNER JOIN public.dmc ON (stock.fno = dmc.fno)
                           WHERE stock.fno = %s;
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
    def convert_stock(self, brand, fno):
        cursor = self.conn.cursor()

        if brand == BRANDS[0]:
            cursor.execute("""
                           SELECT DISTINCT dmc_to_anchor.dmc, stock.fno "anchor", dmc_to_anchor.hex
                           FROM public.stock INNER JOIN public.dmc_to_anchor ON (dmc_to_anchor.anchor = stock.fno)
                           WHERE dmc_to_anchor.dmc = 'White';
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
                        FROM public.dmc_to_anchor
                        WHERE dmc_to_anchor.dmc = %s;
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
                       SELECT * FROM public.stock 
                       WHERE stock.brand = %s AND stock.fno = %s;
                       """, 
                       (brand, fno,))
        
        if cursor.fetchone():
            cursor.close()
            return False

        else:
            cursor.execute("""
                           INSERT INTO public.stock (brand, fno)
                           VALUES (%s, %s);
                           """,
                           (brand, fno))
            self.conn.commit()

            cursor.close()
            return True
        
    # Deletes from stock
    def delete(self, brand, fno):
        cursor = self.conn.cursor()

        cursor.execute("""
                       SELECT * FROM public.stock 
                       WHERE stock.brand = %s AND stock.fno = %s;
                       """, 
                       (brand, fno,))
        
        if cursor.fetchone():
            cursor.execute("""
                           DELETE FROM public.stock
                           WHERE stock.brand = %s AND stock.fno = %s;
                           """,
                          (brand, fno))
            self.conn.commit()
            
            cursor.close()
            return True   
        
        else: 
            cursor.close()
            return False  

    # Checks validity of input
    def input_validation(self, brand, fno):
        if brand in BRANDS:
        
            cursor = self.conn.cursor()
            
            if brand == BRANDS[0]:
                cursor.execute("""
                            SELECT * FROM public.dmc
                            WHERE dmc.fno = %s;
                            """,
                            (fno,))
            
                output = cursor.fetchone()
                if not output:
                    return False

            return True
        return False