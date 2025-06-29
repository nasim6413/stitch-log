from flask import Blueprint, render_template, session, request, redirect, url_for
from stitchlog.models import setup, floss, stock

s = Blueprint('stock', __name__, url_prefix='/stock')

# Stock page
@s.route('/', methods=['GET', 'POST'])
def stock_page():
    conn = setup.get_db()
    session.clear()
    
    if request.method == 'POST':
        item = request.form['floss'].strip()
        
        brand, fno = floss.fix_floss_input(item)
        
        if brand and fno:
            action = request.form['button']
            
            if action == 'add':
                stock.stock_add(conn, brand, fno)
            if action == 'delete':
                stock.stock_del(conn, brand, fno)
            
            return redirect(url_for('stock.stock_page'))
        
        else:
            return redirect(url_for('stock.stock_page'))
        
    rows = stock.stock_list(conn)
    return render_template('stock.html', rows=rows)