from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback() # To make sure that DB accessed made now don't interfere with an error made before
    return render_template('500.html'), 500