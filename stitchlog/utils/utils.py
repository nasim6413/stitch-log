import re
BRANDS = ['DMC', 'Anchor']
FLOSS_PATTERN = r'(DMC|Anchor)\s*(\w?\d{1,4}|B5200|ECRU|White)'

def validate_floss_input(item):
    
    """Input validation for floss entries."""
    
    match = re.match(FLOSS_PATTERN, item, re.IGNORECASE)
    
    return match if match else False

def natural_key(s):
    """Natural sorting for floss lists."""
    s = str(s)
    parts = []
    
    for t in re.split(r'(\d+)', s):
        if t.isdigit():
            parts.append(int(t))
        else:
            parts.append(t.lower())
    return parts