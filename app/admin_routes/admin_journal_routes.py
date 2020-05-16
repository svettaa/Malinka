from flask import render_template, request
from flask_login import login_required

from app import app
from app.api.api_appointment import *
from app.login import admin_only


@app.route('/journal')
@login_required
@admin_only
def journal_get():
    return render_template('journal.html')

