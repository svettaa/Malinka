from sqlalchemy.exc import IntegrityError

from app import db
from app.models import AppointmentPaint


def get_appointment_paints(appointment_id: int):
    return db.engine.execute('SELECT Paint.code AS paint_code, '
                             '       Paint.name AS paint_name, '
                             '       Paint.id AS paint_id, '
                             '       volume_ml '
                             'FROM Appointment_Paint INNER JOIN Paint '
                             '     ON Paint.id = Appointment_Paint.paint_id '
                             'WHERE appointment_id = %s '
                             'ORDER BY paint_id;',
                             appointment_id).fetchall()


def get_appointment_paint(appointment_id: int, paint_id: int):
    return db.engine.execute('SELECT Paint.code AS paint_code, '
                             '       Paint.name AS paint_name, '
                             '       paint_id, appointment_id, '
                             '       volume_ml '
                             'FROM Appointment_Paint INNER JOIN Paint '
                             '     ON Paint.id = Appointment_Paint.paint_id '
                             'WHERE appointment_id = %s AND paint_id = %s '
                             'ORDER BY paint_id;',
                             (appointment_id, paint_id)).fetchone()


def update_appointment_paint(appointment_paint: AppointmentPaint):
    if appointment_paint.volume_ml <= 0:
        return False, 'Кількість має бути більше нуля'
    try:
        # old_amount = db.engine.execute('SELECT volume_ml '
        #                                'FROM Appointment_Paint '
        #                                'WHERE id = %s;',
        #                                supply.id).fetchone()['amount']
        db.engine.execute('UPDATE Appointment_Paint '
                          'SET volume_ml = %s '
                          'WHERE appointment_id = %s AND paint_id = %s;',
                          (appointment_paint.volume_ml,
                           appointment_paint.appointment_id,
                           appointment_paint.paint_id))
        # db.engine.execute('UPDATE Paint '
        #                   'SET left_ml = left_ml - %s '
        #                   'WHERE id = %s',
        #                   (old_amount, supply.paint_id))
        # db.engine.execute('UPDATE Paint '
        #                   'SET left_ml = left_ml + %s '
        #                   'WHERE id = %s',
        #                   (supply.amount, supply.paint_id))
        return True, 'Успішно оновлено використання фарби'
    except IntegrityError:
        return False, 'Порушення цілісності використання фарби'


def add_appointment_paint(appointment_paint: AppointmentPaint):
    if appointment_paint.volume_ml <= 0:
        return False, 'Кількість має бути більше нуля'
    try:
        db.engine.execute('INSERT INTO Appointment_Paint (appointment_id, paint_id, volume_ml) '
                          'VALUES (%s, %s, %s);',
                          (appointment_paint.appointment_id, appointment_paint.paint_id, appointment_paint.volume_ml))
        # db.engine.execute('UPDATE Paint '
        #                   'SET left_ml = left_ml + %s '
        #                   'WHERE id = %s',
        #                   (supply.amount, supply.paint_id))
        return True, 'Успішно додано використання фарби'
    except IntegrityError:
        return False, 'Порушення цілісності використання фарби'


def delete_appointment_paint(appointment_id: int, paint_id: int):
    try:
        # old = db.engine.execute('SELECT amount, paint_id '
        #                         'FROM Paint_Supply '
        #                         'WHERE id = %s;',
        #                         supply_id).fetchone()
        db.engine.execute('DELETE '
                          'FROM Appointment_Paint '
                          'WHERE appointment_id = %s AND paint_id = %s;',
                          (appointment_id, paint_id))
        # db.engine.execute('UPDATE Paint '
        #                   'SET left_ml = left_ml - %s '
        #                   'WHERE id = %s',
        #                   (old['amount'], old['paint_id']))
        return True, 'Успішно видалено використання фарби'
    except IntegrityError:
        return False, 'Порушення цілісності використання фарби'
