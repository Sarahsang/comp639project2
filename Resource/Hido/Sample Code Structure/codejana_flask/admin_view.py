from codejana_flask import app
from flask import render_template

@app.route('/admin')
def admin():
    return "admin"