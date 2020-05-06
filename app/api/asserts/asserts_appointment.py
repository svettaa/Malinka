import pytz
from datetime import datetime, date, time

from app import db
from app.models import Appointment


def is_future_appointment(appointment: Appointment):
    appoint_start = pytz.timezone('Europe/Kiev').localize(appointment.appoint_start)
    now = datetime.now(pytz.timezone('Europe/Kiev'))
    return appoint_start > now


def assert_appointment_is_hired(appointment: Appointment):
    if is_future_appointment(appointment) and \
            not db.session.execute(""" SELECT is_hired
                                       FROM Master
                                       WHERE id = :master_id;
                                   """,
                                   {'master_id': appointment.master_id}).scalar():
        raise AssertionError('Даний майстер звільнений')
