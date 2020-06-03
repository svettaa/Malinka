from app import db
from app.models import AppointmentPaint


def assert_paint_enough(paint_id: int):
    if db.session.execute('SELECT left_ml '
                          'FROM Paint '
                          'WHERE id = :paint_id;',
                          {'paint_id': paint_id}).scalar() < 0:
        raise AssertionError('Неможливо виконати операцію, недостатньо фарби')


def assert_appointment_not_uses_paint(appointment_paint: AppointmentPaint):
    if db.session.execute('SELECT COUNT(*) '
                          'FROM Appointment_Paint '
                          'WHERE paint_id = :paint_id AND '
                          '      appointment_id = :appointment_id;',
                          {'paint_id': appointment_paint.paint_id,
                           'appointment_id': appointment_paint.appointment_id}).scalar() > 0:
        raise AssertionError('В даному записі вже використовується дана фарба')


def assert_appointment_uses_paint(appointment_paint: AppointmentPaint):
    if db.session.execute('SELECT COUNT(*) '
                          'FROM Appointment_Paint '
                          'WHERE paint_id = :paint_id AND '
                          '      appointment_id = :appointment_id;',
                          {'paint_id': appointment_paint.paint_id,
                           'appointment_id': appointment_paint.appointment_id}).scalar() == 0:
        raise AssertionError('Запис не використовує дану фарбу')
