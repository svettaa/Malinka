from datetime import datetime, date, time

from app import db
from app.models import Appointment


def is_future_appointment(appointment: Appointment):
    return (appointment.appoint_date.date() > datetime.now().date() or
            (appointment.appoint_date.date() == datetime.now().date() and
             appointment.start_time.time() > datetime.now().time()))


def assert_appointment_is_hired(appointment: Appointment):
    if is_future_appointment(appointment) and \
            not db.session.execute(""" SELECT is_hired
                                       FROM Master
                                       WHERE id = :master_id;
                                   """,
                                   {'master_id': appointment.master_id}).scalar():
        raise AssertionError('Даний майстер звільнений')
