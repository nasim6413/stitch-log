import psycopg2

BRANDS = ['DMC', 'Anchor']

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
        
        output = cursor.fetchall()

        if output:
            cursor.close()
            return output

        else:
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

        if brand == 'DMC':
            cursor.execute("""
                        SELECT stock.*, dmc.name, dmc.hex
                        FROM public.stock INNER JOIN public.dmc ON (stock.fno = dmc.fno)
                        WHERE stock.fno = %s;
                        """, 
                        (fno,))

        output = cursor.fetchall()
        
        if output:
            cursor.close()
            return output
        
        else:
            return False
        
    # Returns possible conversions for specified floss number according to what is available in stock        
    def convert_stock(self, brand, fno):
        cursor = self.conn.cursor()

        cursor.execute("""
                    SELECT DISTINCT dmc_to_anchor.dmc, stock.fno, dmc_to_anchor.hex
                    FROM public.stock INNER JOIN public.dmc_to_anchor ON (stock.fno = dmc_to_anchor.anchor)
                    WHERE dmc_to_anchor.dmc = %s;
                    """,
                    (fno,))
        
        output = cursor.fetchall()
        
        if output:
            cursor.close()
            return output
                
        else:
            cursor.close()
            return False
    
    # Returns possible conversion for specified floss number
    def convert(self, brand, fno):
        cursor = self.conn.cursor()

        if brand == 'Anchor':
            print('Currently unavailable.')

        if brand == 'DMC':
            cursor.execute("""
                        SELECT dmc, anchor, hex
                        FROM public.dmc_to_anchor
                        WHERE dmc_to_anchor.dmc = %s;
                        """,
                        (fno,))
            
            output = cursor.fetchall()
            
            if output:
                cursor.close()
                return output

            else:
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
        if brand not in BRANDS:
            return False
        
        cursor = self.conn.cursor()
        
        if brand == 'DMC':
            cursor.execute("""
                        SELECT * FROM public.dmc
                        WHERE dmc.fno = %s;
                        """,
                        (fno,))
        
            output = cursor.fetchone()
            if not output:
                return False
        
        return True