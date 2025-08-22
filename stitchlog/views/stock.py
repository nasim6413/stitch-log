from flask import Blueprint, render_template, request, jsonify
from stitchlog.models import setup, floss, stock

s = Blueprint('stock', __name__, url_prefix='/stock')

@s.route('/', methods=['GET'])
def stock_page():
    return render_template('stock.html')

@s.route('/list', methods=['GET'])
def stock_list():
    conn = setup.get_db()
    rows = stock.stock_list(conn)
    return jsonify([{"brand": r[0], "fno": r[1]} for r in rows])

@s.route('/add', methods=['POST'])
def stock_add_item():
    conn = setup.get_db()
    data = request.get_json()
    item = data.get('floss', '').strip()

    brand, fno = floss.fix_floss_input(item)
    
    if brand and fno:
        stock.stock_add(conn, brand, fno)
        return jsonify({"status": "ok"})
    return jsonify({"status": "error", "message": "Invalid input!"}), 400

@s.route('/delete', methods=['POST'])
def stock_delete_item():
    conn = setup.get_db()
    data = request.get_json()
    item = data.get('floss', '').strip()

    brand, fno = floss.fix_floss_input(item)
    
    if brand and fno:
        stock.stock_del(conn, brand, fno)
        return jsonify({"status": "ok"})

    return jsonify({"status": "error", "message": "Invalid input!"}), 400
