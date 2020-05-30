from flask import render_template, request, redirect, url_for
from flask_login import login_required

from app import app
from app.forms import AdminProcedureForm
from app.api.api_procedure import *
from app.api.api_category import get_categories
from app.login import admin_only


@app.route('/procedures')
@login_required
@admin_only
def procedures_get():
    return render_template('procedures.html', csrf_token=AdminProcedureForm().csrf_token)
