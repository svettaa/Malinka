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


def assert_appointment_overlaps_master(appointment: Appointment):
    if db.session.execute(""" SELECT COUNT(*)
                                  FROM Appointment
                                  WHERE (master_id = :master_id OR client_id = :master_id)
                                        AND
                                        (appoint_start, appoint_end) 
                                        OVERLAPS
                                        (:appoint_start, :appoint_end);
                              """,
                          {'master_id': appointment.master_id,
                           'appoint_start': appointment.appoint_start,
                           'appoint_end': appointment.appoint_end}).scalar() > 1:
        raise AssertionError('Даний запис перетинається з іншими записами майстра')


def assert_appointment_overlaps_client(appointment: Appointment):
    if db.session.execute(""" SELECT COUNT(*)
                                  FROM Appointment
                                  WHERE (master_id = :client_id OR client_id = :client_id)
                                        AND
                                        (appoint_start, appoint_end) 
                                        OVERLAPS
                                        (:appoint_start, :appoint_end);
                              """,
                          {'client_id': appointment.client_id,
                           'appoint_start': appointment.appoint_start,
                           'appoint_end': appointment.appoint_end}).scalar() > 1:
        raise AssertionError('Даний запис перетинається з іншими записами клієнта')
