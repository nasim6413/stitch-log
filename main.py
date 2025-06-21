import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g
from database import setup, stock, projects, convert

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('floss.db')
    return g.db
    
@app.route('/')
@app.route('/home')
def home_page():
    conn = get_db()
    stock_count = stock.stock_count(conn)

    return render_template('home.html', stock_count=stock_count)

# Stock page
@app.route('/stock', methods=['GET', 'POST'])
def stock_page():
    conn = get_db()
    
    if request.method == 'POST':
        item = request.form['floss']
        
        if item:
            brand, fno = setup.re_input(item)
            
            action = request.form['button']
            
            if action == 'add':
                stock.stock_add(conn, brand, fno)
            if action == 'delete':
                stock.stock_del(conn, brand, fno)
            
            return redirect(url_for('stock_page'))
        else:
            return redirect(url_for('stock_page'))
        
    rows = stock.stock_list(conn)
    return render_template('stock.html', rows=rows)

# Conversion page
@app.route('/convert', methods=['GET', 'POST'])
def convert_page():
    conn = get_db()
    
    if request.method == 'POST':
        item = request.form['floss']
        
        if item:
            brand, fno = setup.re_input(item)
                                   
            converted_brand, rows = convert.gen_convert(conn, brand, fno)
                
        return render_template('convert.html', brand=brand, converted_brand=converted_brand, rows=rows)
    
    return render_template('convert.html')

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close()

if __name__ == '__main__':
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            setup.set_up(conn)

        conn.commit()
        cursor.close()
        conn.close()
        
    app.run()