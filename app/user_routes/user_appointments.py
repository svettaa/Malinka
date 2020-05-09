from flask import render_template
from flask_login import login_required

from app import app


@app.route('/cabinet/appointments', methods=['GET'])
@login_required
def user_appointments_get():
    return render_template('user_appointments.html')