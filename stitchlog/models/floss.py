from ..utils.utils import *
    
def fix_floss_input(item):
    """Validates and fixes floss input."""
    match = re.match(FLOSS_PATTERN, item, re.IGNORECASE)

    if match:
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
    
    else:
        return False, False
    
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