from flask import Blueprint, render_template, redirect, url_for, request, current_app
from stitchlog.models import setup, stock, projects

h = Blueprint('home', __name__)

@h.route('/', methods=['GET', 'POST'])
@h.route('/home', methods=['GET', 'POST'])
def home_page():
    conn = setup.get_db()
    username = setup.get_username()

    if not username and request.method == 'POST':
        username = request.form['username']
        
        setup.set_username(current_app, username) # Username setup if not existing

        return redirect(url_for('home.home_page'))
        
    floss_count = len(stock.stock_list(conn))
    project_count = len(projects.list_project_details(conn))

    return render_template('home.html', username=username, floss_count=floss_count, project_count=project_count)