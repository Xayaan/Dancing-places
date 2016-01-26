import sessions
from flask import render_template
from app import app
from flask.ext.login import current_user

@app.errorhandler(404)
def page_not_found(e):
    return "404 Error"

@app.errorhandler(500)
def page_not_found(e):
    return "500 Error"