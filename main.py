from flask import Flask, render_template, request, redirect, url_for, g
from database import Database


app = Flask(__name__)
floss = Database()

def get_db():
    if 'db' not in g:
        g.db = floss.connect()
        return g.db if g.db else False

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    conn = get_db()
    count = floss.stock_count(conn)
    
    if request.method == 'POST':
        item = request.form['floss']
        
        if item:
            brand, fno = floss.re_input(item)
            action = request.form['button']
            
            if action == 'search':
                rows = floss.search(conn, brand, fno)
                
                if rows:
                    message = f'Floss {brand} {fno} in stock!'
                    return render_template('home.html', message=message, count=count)
                
                else:
                    rows = floss.stock_convert(conn, brand, fno)
                    
                    if rows:
                        message = f'Floss {brand} {fno} not in stock. Possible conversions available:'
                    
                    else:
                        message = f'Floss {brand} {fno} not in stock and no possible conversions are available.'
                        
            if action == 'convert':
                rows = floss.gen_convert(conn, brand, fno)
                message = f'Possible conversions for floss {brand} {fno}:'
                
        return render_template('home.html', message=message, count=count, rows=rows)
    
    return render_template('home.html', count=count)

# Stock page
@app.route('/stock', methods=['GET', 'POST'])
def stock():
    conn = get_db()
    
    if request.method == 'POST':
        item = request.form['floss']
        
        if item:
            brand, fno = floss.re_input(item)
            
            action = request.form['button']
            
            if action == 'add':
                floss.add(conn, brand, fno)
            if action == 'delete':
                floss.delete(conn, brand, fno)
            
            return redirect(url_for('stock'))
        else:
            return redirect(url_for('stock'))
        
    rows = floss.flist(conn)
    return render_template('stock.html', rows=rows)

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()