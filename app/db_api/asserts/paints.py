from datetime import datetime

import pytz
from sqlalchemy.orm import Session

from app import db
from app.models import AppointmentPaint, PaintSupply


def is_before_today_supply(supply: PaintSupply):
    supply_date = supply.supply_date.date()
    now = datetime.now(pytz.timezone('Europe/Kiev')).date()
    return supply_date <= now


def assert_paint_enough(paint_id: int, session: Session):
    if session.execute('SELECT left_ml '
                       'FROM Paint '
                       'WHERE id = :paint_id;',
                       {'paint_id': paint_id}).scalar() < 0:
        raise AssertionError('Неможливо виконати операцію, недостатньо фарби')


def assert_paint_supply_before_today(supply: PaintSupply):
    if not is_before_today_supply(supply):
        raise AssertionError('Неможливо вказати поставку у майбутньому')


def assert_appointment_not_uses_paint(appointment_paint: AppointmentPaint, session: Session):
    if session.execute('SELECT COUNT(*) '
                       'FROM Appointment_Paint '
                       'WHERE paint_id = :paint_id AND '
                       '      appointment_id = :appointment_id;',
                       {'paint_id': appointment_paint.paint_id,
                        'appointment_id': appointment_paint.appointment_id}).scalar() > 0:
        raise AssertionError('В даному записі вже використовується дана фарба')


def assert_appointment_not_future_for_paints(appointment_paint: AppointmentPaint, session: Session):
    if session.execute('SELECT appoint_start > now() '
                       'FROM Appointment '
                       'WHERE id = :id;',
                       {'id': appointment_paint.appointment_id}).scalar():
        raise AssertionError('Неможливо додати фарби до запису, що не відбувся')


def assert_appointment_procedure_uses_paint(appointment_paint: AppointmentPaint, session: Session):
    if not session.execute('SELECT uses_paints '
                           'FROM Appointment INNER JOIN Procedure ON procedure_id = Procedure.id '
                           'WHERE Appointment.id = :appointment_id;',
                           {'appointment_id': appointment_paint.appointment_id}).scalar():
        raise AssertionError('Процедура даного запису не дозволяє використання фарб')


def assert_appointment_uses_paint(appointment_paint: AppointmentPaint, session: Session):
    if session.execute('SELECT COUNT(*) '
                       'FROM Appointment_Paint '
                       'WHERE paint_id = :paint_id AND '
                       '      appointment_id = :appointment_id;',
                       {'paint_id': appointment_paint.paint_id,
                        'appointment_id': appointment_paint.appointment_id}).scalar() == 0:
        raise AssertionError('Запис не використовує дану фарбу')
