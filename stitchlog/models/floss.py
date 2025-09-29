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
    
def floss_convert(conn, brand, fno):
    """Returns all possible conversions for a specified floss and whether available."""
    cursor = conn.cursor()

    if brand == BRANDS[0]:
        converted = BRANDS[1]
    else:
        converted = BRANDS[0]
        
    cursor.execute(f"""
                   SELECT 
                        conversions.{brand.lower()}, 
                        conversions.{converted.lower()},
                        conversions.colour,
                        conversions.hex, 
                        (stock.stock_id IS NOT NULL) as available
                    FROM conversions
                    LEFT JOIN stock 
                        ON stock.brand = ?
                        AND stock.f_no = conversions.{converted}
                    WHERE conversions.{brand.lower()} = ?;
                    """,
                    (converted, fno,))
        
    try:
        output = cursor.fetchall()
        cursor.close()
        return converted, output

    except:
        cursor.close()
        return False