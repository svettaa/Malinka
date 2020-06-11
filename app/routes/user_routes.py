from flask import render_template, request
from flask_login import login_required, current_user

from app import app
from app.forms import AdminClientForm
from app.db_api.appointments import get_client_future_appointments, delete_appointment_if_future, \
    get_client_past_appointments


@app.route('/profile', methods=['GET'])
@login_required
def edit_user_profile_get():
    return render_template('user/profile.html', csrf_token=AdminClientForm().csrf_token)


@app.route('/profile/appointments', methods=['GET'])
@login_required
def user_appointments_get():
    return render_template('user/appointments.html', csrf_token=AdminClientForm().csrf_token,
                           future_appointments=get_client_future_appointments(current_user.id),
                           past_appointments=get_client_past_appointments(current_user.id),
                           error=(request.args.get('error')),
                           success=(request.args.get('success')))
