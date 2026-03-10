from ..utils.utils import *
    
def fix_floss_input(item):
    """Validates and fixes floss input."""
    match = re.match(FLOSS_PATTERN, item, re.IGNORECASE)

    if match:        
        item = match.group(0)  # take the matched text
        
        if item.capitalize() == 'White' or item.capitalize() == 'Ecru':
            item = item.capitalize()
            
        return item

    return False
    
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