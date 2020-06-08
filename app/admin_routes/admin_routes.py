from flask import render_template
from flask_login import login_required

from app import app
from app.forms import *
from app.login import admin_only


@app.route('/journal')
@login_required
@admin_only
def journal_get():
    return render_template('admin/journal.html')


@app.route('/statistics', methods=['GET'])
@login_required
@admin_only
def statistics_get():
    return render_template('admin/statistics.html')


@app.route('/paints', methods=['GET'])
@login_required
@admin_only
def paints_get():
    return render_template('admin/paints.html', csrf_token=AdminPaintForm().csrf_token)


@app.route('/procedures')
@login_required
@admin_only
def procedures_get():
    return render_template('admin/procedures.html', csrf_token=AdminProcedureForm().csrf_token)


@app.route('/categories')
@login_required
@admin_only
def categories_get():
    return render_template('admin/categories.html', csrf_token=AdminCategoryForm().csrf_token)


@app.route('/appointments')
@login_required
@admin_only
def appointments_get():
    return render_template('admin/appointments.html', csrf_token=AdminAppointmentForm().csrf_token)


@app.route('/supplies')
@login_required
@admin_only
def supplies_get():
    return render_template('admin/supplies.html', csrf_token=AdminSupplyForm().csrf_token)
