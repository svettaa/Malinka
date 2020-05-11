from flask import render_template, request
from flask_login import login_required

from app import app
from app.api.api_paint import *
from app.login import admin_only


@app.route('/statistics', methods=['GET'])
@login_required
@admin_only
def statistics_get():
    return render_template('statistics.html', paints=get_paints())