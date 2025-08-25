from pypdf import PdfReader
from io import BytesIO
# from .helpers import FLOSS_PATTERN
import re

# def validate_upload(file):


def extract_floss(file):
    reader = PdfReader(file)
    pattern = re.compile(r'(DMC|Anchor)\s*(\w?\d{1,4}|B5200|ECRU|White)')

    floss_list = []

    for page in reader.pages:
        text = page.extract_text()
        
        if text:
            matches = pattern.findall(text)
            floss_list.extend(matches)
            
    floss_list = sorted(set(floss_list))
    return floss_list