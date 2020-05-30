from flask import render_template, request, redirect, url_for
from flask_login import login_required

from app import app
from app.api.api_appointment import *
from app.api.api_client import get_clients
from app.api.api_master import get_masters
from app.api.api_procedure import get_procedures
from app.api.api_appointment_paint import get_appointment_paints
from app.forms import AdminAppointmentForm
from app.login import admin_only


@app.route('/appointments')
@login_required
@admin_only
def appointments_get():
    return render_template('appointments.html', csrf_token=AdminAppointmentForm().csrf_token)
