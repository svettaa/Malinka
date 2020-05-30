from flask import render_template
from flask_login import login_required

from app import app
from app.forms import AdminAppointmentForm
from app.login import admin_only


@app.route('/appointments')
@login_required
@admin_only
def appointments_get():
    return render_template('appointments.html', csrf_token=AdminAppointmentForm().csrf_token)
