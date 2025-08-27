from flask import jsonify

def success_response(data=None, status_code=200):
    return jsonify({
        "status": "ok",
        "data": data
    }), status_code

def error_response(message, status_code=400):
    return jsonify({
        "status": "error",
        "message": message
    }), status_code