import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session

from app import db
from app.models import Appointment


def is_future_appointment(appointment: Appointment):
    appoint_start = appointment.appoint_start
    now = datetime.now(pytz.timezone('Europe/Kiev'))
    return appoint_start > now


def assert_appointment_is_future(appointment_id: int):
    if not db.session.execute('SELECT appoint_start > now() '
                              'FROM Appointment '
                              'WHERE id = :id;',
                              {'id': appointment_id}).scalar():
        raise AssertionError('Запис вже відбувся')


def assert_appointment_client(appointment: Appointment, user_id: int):
    if appointment.client_id != user_id:
        raise AssertionError('Спроба видалити чужі записи')


def assert_appointment_is_hired(appointment: Appointment, session: Session):
    if is_future_appointment(appointment) and \
            not session.execute(""" SELECT is_hired
                                       FROM Master
                                       WHERE id = :master_id;
                                   """,
                                {'master_id': appointment.master_id}).scalar():
        raise AssertionError('Даний майстер звільнений')


def assert_appointment_no_overlaps_master(appointment: Appointment, session: Session):
    if session.execute(""" SELECT COUNT(*)
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


def assert_appointment_no_overlaps_client(appointment: Appointment, session: Session):
    if session.execute(""" SELECT COUNT(*)
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


def assert_appointment_even_schedule_or_working(appointment: Appointment, session: Session):
    if not is_future_appointment(appointment):
        return
    day = appointment.appoint_start.day
    even_day = (day % 2 == 0)
    master_even_schedule = session.execute('SELECT even_schedule '
                                           'FROM Master '
                                           'WHERE id = :master_id;',
                                           {'master_id': appointment.master_id}).scalar()
    if even_day == master_even_schedule:
        return
    # not master's schedule, looking for working changes
    if session.execute('SELECT COUNT(*) '
                       'FROM Schedule_Change '
                       'WHERE Schedule_Change.master_id = :master_id '
                       '      AND is_working = True AND '
                       '      change_start <= :appoint_start AND '
                       '      change_end >= :appoint_end;',
                       {'master_id': appointment.master_id,
                        'appoint_start': appointment.appoint_start,
                        'appoint_end': appointment.appoint_end}).scalar() == 0:
        raise AssertionError('Майстер не працює у цей час')


def assert_appointment_master_does_procedure(appointment: Appointment, session: Session):
    if not is_future_appointment(appointment):
        return
    if session.execute("""     SELECT COUNT(*)
                                  FROM Master_Procedure
                                  WHERE master_id = :master_id 
                                        AND
                                        procedure_id = :procedure_id;
                              """,
                       {'master_id': appointment.master_id,
                        'procedure_id': appointment.procedure_id}).scalar() == 0:
        raise AssertionError('Даний майстер не вміє виконувати дану процедуру')


def assert_appointment_master_no_vacation(appointment: Appointment, session: Session):
    if session.execute('SELECT COUNT(*) '
                       'FROM Schedule_Change '
                       'WHERE master_id = :master_id AND '
                       '      is_working = False AND '
                       '      (change_start, change_end) '
                       '      OVERLAPS '
                       '      (:appoint_start, :appoint_end);',
                       {'master_id': appointment.master_id,
                        'appoint_start': appointment.appoint_start,
                        'appoint_end': appointment.appoint_end}).scalar() > 0:
        raise AssertionError('У майстра відпустка на цей час')


def assert_client_has_not_many_future_appointments(appointment: Appointment, session: Session):
    if session.execute('SELECT COUNT(*) '
                       'FROM Appointment '
                       'WHERE client_id = :client_id AND '
                       '      appoint_start > now();',
                       {'client_id': appointment.client_id}).scalar() > 2:
        raise AssertionError('Клієнт не може мати більше 2 невиконаних записів')


def assert_appointment_is_in_nearest_future(appointment: Appointment):
    appoint_start = appointment.appoint_start.date()
    now = datetime.now(pytz.timezone('Europe/Kiev')).date()
    max_possible_start = now + relativedelta(months=2)
    if appoint_start > max_possible_start:
        raise AssertionError('Запис має бути протягом двох місяців від сьогодні')
