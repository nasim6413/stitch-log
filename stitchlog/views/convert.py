from flask import Blueprint, render_template, session, request, redirect, url_for
from stitchlog.models import setup, convert

c = Blueprint('convert', __name__, url_prefix='/convert')

# Conversion page
@c.route('/', methods=['GET', 'POST'])
def convert_page():
    conn = setup.get_db()
    session.clear()
    
    if request.method == 'POST':
        item = request.form['floss'].strip()
        
        if setup.validate_floss_input(item):
            brand, fno = setup.fix_input(item)
                                   
            converted_brand, rows = convert.gen_convert(conn, brand, fno)
                
            return render_template('convert.html', brand=brand, converted_brand=converted_brand, rows=rows)
        
        else:
            return redirect(url_for('convert.convert_page'))
    
    return render_template('convert.html')