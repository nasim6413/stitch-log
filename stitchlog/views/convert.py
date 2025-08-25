from flask import Blueprint, render_template, jsonify
from stitchlog.models import floss, setup
from ..utils.responses import *

c = Blueprint('convert', __name__, url_prefix='/convert')

@c.route('/', methods=['GET'])
def convert_page():
    return render_template('convert_page.html')

@c.route('/<item>', methods=['GET'])
def converted_input(item):
    item = item.strip()
    brand, fno = floss.fix_floss_input(item)
    
    if brand or fno:
        return success_response(
            {
            "brand": brand,
            "fno": fno
            }
        )
                
    else:
        return error_response("Invalid input!")
    
@c.route('/<brand>-<fno>', methods=['GET'])
def converted_page(brand, fno):
    conn = setup.get_db()
    converted_brand, rows = floss.gen_convert(conn, brand, fno)

    if rows:
        return success_response([
            {
                "brand" : brand,
                "brand_fno": r[0],
                "converted_brand" : converted_brand,
                "converted_fno": r[1],
                "hex": r[2],
                "availability": r[3]
            } for r in rows
        ])
        
    else:
        return error_response("Conversion does not exist!")