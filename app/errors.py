from flask import render_template
from app import app, db

@app.errorhandler(403)
def not_found_error(error):
    return render_template('errors/403.html'), 403
