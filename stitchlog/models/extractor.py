from pypdf import PdfReader
from io import BytesIO
from ..utils.utils import FLOSS_PATTERN
import re

def validate_upload(file):

    """Validates PDF pattern file upload."""

    if file.filename == '':
        return False
    
    if not file.filename.lower().endswith('.pdf'):
        return False
    
    else:
        return True

def extract_floss(file):

    """Extracts floss from PDF pattern."""
    
    pattern_file = BytesIO(file.read())
    reader = PdfReader(pattern_file)
    pattern = re.compile(FLOSS_PATTERN)

    floss_list = []

    for page in reader.pages:
        text = page.extract_text()
        
        if text:
            matches = pattern.findall(text)

            for match in matches:               
                floss_list.append(f'{match[0]} {match[1]}')
            
    floss_list = sorted(set(floss_list))
    return floss_list