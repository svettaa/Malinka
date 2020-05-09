from flask import render_template

from app import app


@app.route('/cabinet/appointments', methods=['GET'])
def user_appointments_get():
    return render_template('user_appointments.html')