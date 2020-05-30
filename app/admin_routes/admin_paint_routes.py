from flask import render_template
from flask_login import login_required

from app import app
from app.forms import AdminPaintForm
from app.api.api_paint import *
from app.login import admin_only


@app.route('/paints', methods=['GET'])
@login_required
@admin_only
def paints_get():
    return render_template('paints.html', paints=get_paints(), csrf_token=AdminPaintForm().csrf_token)