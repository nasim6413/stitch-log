from flask import Blueprint, render_template, session, request, redirect, url_for
from stitchlog.models import floss, setup

c = Blueprint('convert', __name__, url_prefix='/convert')

# Conversion page
@c.route('/', methods=['GET', 'POST'])
def convert_page():
    conn = setup.get_db()
    session.clear()
    
    if request.method == 'POST':
        item = request.form['floss'].strip()
        
        brand, fno = floss.fix_floss_input(item)

        if brand and fno:
            converted_brand, rows = floss.gen_convert(conn, brand, fno)

            if not rows:
                error = f'Conversion does not exist.'
                return render_template('convert.html', error=error)

            else:
                return render_template('convert.html', brand=brand, converted_brand=converted_brand, rows=rows)
        
        else:
            error = f'Please input valid floss.'
            return render_template('convert.html', error=error)
    
    return render_template('convert.html')