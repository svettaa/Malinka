from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user

from app import app
from app.api.api_appointment import get_client_future_appointments, delete_appointment_if_future, \
    get_client_past_appointments


@app.route('/cabinet/appointments', methods=['GET'])
@login_required
def user_appointments_get():
    return render_template('user_appointments.html',
                           future_appointments=get_client_future_appointments(current_user.id),
                           past_appointments=get_client_past_appointments(current_user.id),
                           error=(request.args.get('error')),
                           success=(request.args.get('success')))


@app.route('/cabinet/appointments/delete/<int:appointment_id>', methods=['GET'])
@login_required
def delete_user_appointment_get(appointment_id):
    status, message = delete_appointment_if_future(appointment_id, current_user.id)

    if status:
        return redirect(url_for('user_appointments_get',
                                success=message))
    else:
        return redirect(url_for('user_appointments_get',
                                error=message))
