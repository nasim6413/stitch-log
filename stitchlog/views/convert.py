from flask import Blueprint, render_template, jsonify
from stitchlog.models import floss, setup
from ..utils.responses import *

c = Blueprint('convert', __name__, url_prefix='/convert')

@c.route('/', methods=['GET'])
def convert_page():
    return render_template('convert.html')

@c.route('/<item>', methods=['GET'])
def converted_input(item):
    """Validates and fixes floss input."""
    item = item.strip()
    brand, fno = floss.fix_floss_input(item)
    
    if not (brand and fno):
        return error_response("Invalid input!")
    
    fixed_input = {
        "brand": brand,
        "fno" : fno
    }
    return success_response(fixed_input)
    
@c.route('/<brand>-<fno>', methods=['GET'])
def converted_page(brand, fno):
    """Converts floss input from one brand to another."""
    conn = setup.get_db()
    converted_brand, rows = floss.gen_convert(conn, brand, fno)

    if not rows:
        return error_response("Conversion does not exist!")
    
    else:
        result = [
            {
                "brand" : brand,
                "brand_fno": row[0],
                "converted_brand" : converted_brand,
                "converted_fno": row[1],
                "hex": row[2],
                "availability": row[3]
            } 
            for row in rows
        ]
        return success_response(result)
    