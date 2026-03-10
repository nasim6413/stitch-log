import re
BRANDS = ['DMC', 'Anchor']
FLOSS_PATTERN = r'\b(?:[A-Z]?\d{1,4}|ECRU|White)'

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