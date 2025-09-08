from flask import Blueprint, render_template, redirect, url_for, request, current_app
from stitchlog.models import setup, stock, projects

h = Blueprint('home', __name__)

@h.route('/', methods=['GET', 'POST'])
@h.route('/home', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')