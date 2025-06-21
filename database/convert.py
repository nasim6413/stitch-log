from .helpers import *

def gen_convert(conn, brand, fno):
    
    """Returns all possible conversions for a specified floss and whether available."""
    
    cursor = conn.cursor()

    if brand == BRANDS[0]:
        cursor.execute("""
                    SELECT dmc_to_anchor.dmc, dmc_to_anchor.anchor, dmc_to_anchor.hex, (stock.id IS NOT NULL) as available
                    FROM dmc_to_anchor
                    LEFT JOIN stock ON stock.brand = 'Anchor' AND dmc_to_anchor.anchor = stock.fno
                    WHERE dmc_to_anchor.dmc = ?;
                    """,
                    (fno,))
        
        converted = BRANDS[1]
        
    if brand == BRANDS[1]:
        cursor.execute("""
                    SELECT anchor_to_dmc.anchor, anchor_to_dmc.dmc, anchor_to_dmc.hex, (stock.id IS NOT NULL) as available
                    FROM anchor_to_dmc
                    LEFT JOIN stock ON stock.brand = 'DMC' AND anchor_to_dmc.dmc = stock.fno
                    WHERE anchor_to_dmc.anchor = ?;
                    """,
                    (fno,))
        
        converted = BRANDS[0]
        
    try:
        output = cursor.fetchall()
        cursor.close()
        return converted, output

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