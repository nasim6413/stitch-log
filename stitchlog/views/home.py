from flask import Blueprint, render_template

h = Blueprint('home', __name__)

@h.route('/')
@h.route('/home')
def home_page():
    return render_template('home.html')