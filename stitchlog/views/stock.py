from flask import Blueprint, render_template, request
from stitchlog.models import setup, floss, stock
from ..models.search import search_stock
from ..utils.responses import *

s = Blueprint('stock', __name__, url_prefix='/stock')

@s.route('/', methods=['GET'])
def stock_page():
    return render_template('stock.html')

@s.route('/list', methods=['GET'])
def stock_list():
    conn = setup.get_db()
    rows = stock.stock_list(conn)
    return success_response([
        {
            "brand": r[0], 
            "fno": r[1]
            } for r in rows
        ]) if rows else error_response("Error in retrieving stock data.")

@s.route('/add', methods=['POST'])
def stock_add_item():
    conn = setup.get_db()
    data = request.get_json()
    item = data.get('floss', '').strip()

    brand, fno = floss.fix_floss_input(item)
    
    if brand and fno:
        if not search_stock(conn, brand, fno):
            result = stock.stock_add(conn, brand, fno)

            return success_response(
                {
                    "brand" : brand,
                    "fno" : fno
                    }
                ) if result else error_response("Error when adding floss.")
            
        else:
            return error_response("Floss already in stock!")
    
    return error_response("Invalid input!")

@s.route('/delete', methods=['POST'])
def stock_delete_item():
    conn = setup.get_db()
    data = request.get_json()
    
    if search_stock(conn, data['brand'], data['fno']):
        result = stock.stock_del(conn, data['brand'], data['fno'])

        return success_response() if result else error_response("Error in deleting floss.")
        
    else:
        return error_response("Floss was not in stock!")
