from pypdf import PdfReader
from io import BytesIO
from ..utils.utils import EXTRACTION_PATTERN
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
    pattern = re.compile(EXTRACTION_PATTERN)

    floss_list = []

    for page in reader.pages:
        text = page.extract_text()
        
        if text:
            matches = pattern.findall(text)

            for match in matches:               
                floss_list.append({
                    "brand": match[0], 
                    "floss": match[1]
                    })

    # De-duplication
    floss_list = list({(i["brand"], i["floss"]): i for i in floss_list}.values())

    print(floss_list)
    return floss_list