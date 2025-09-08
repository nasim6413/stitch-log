from flask import Blueprint, render_template, request
from stitchlog.models import setup, floss, stock
from ..models.search import search_stock
from ..utils.responses import *

s = Blueprint('stock', __name__, url_prefix='/stock')

@s.route('/', methods=['GET'])
def stock_page():
    return render_template('stock.html')

@s.route("/list", methods=["GET"])
def stock_list():
    """Retrieve and return the full stock list of floss items."""
    conn = setup.get_db()
    rows = stock.stock_list(conn)

    if not rows:
        return error_response("Error retrieving stock data.")

    stock_items = [
        {
            "brand": row[0],
            "fno": row[1],
        }
        for row in rows
    ]
    return success_response(stock_items)

@s.route("/add", methods=["POST"])
def stock_add_item():
    """Add a floss item to stock."""
    conn = setup.get_db()
    data = request.get_json()
    item = data.get("floss", "").strip()

    brand, fno = floss.fix_floss_input(item)

    if not (brand and fno):
        return error_response("Invalid input!")

    if search_stock(conn, brand, fno):
        return error_response("Floss already in stock!")

    result = stock.stock_add(conn, brand, fno)
    if not result:
        return error_response("Error adding floss.")

    return success_response({"brand": brand, "fno": fno})

@s.route("/delete", methods=["POST"])
def stock_delete_item():
    """Delete a floss item from stock."""
    conn = setup.get_db()
    data = request.get_json()

    brand, fno = data['brand'], data['fno']

    if not (brand and fno):
        return error_response("Invalid input!")

    if not search_stock(conn, brand, fno):
        return error_response("Floss not in stock!")

    result = stock.stock_del(conn, brand, fno)
    if not result:
        return error_response("Error deleting floss.")

    return success_response()
