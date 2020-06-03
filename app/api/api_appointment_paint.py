from sqlalchemy.exc import IntegrityError

from app import db
from app.api.asserts.asserts_paint import *


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
        assert_appointment_uses_paint(appointment_paint)
        old_amount = db.session.execute('SELECT volume_ml '
                                        'FROM Appointment_Paint '
                                        'WHERE appointment_id = :appointment_id AND paint_id = :paint_id;',
                                        {'appointment_id': appointment_paint.appointment_id,
                                         'paint_id': appointment_paint.paint_id}).scalar()
        db.session.execute('UPDATE Appointment_Paint '
                           'SET volume_ml = :volume_ml '
                           'WHERE appointment_id = :appointment_id AND paint_id = :paint_id;',
                           {'volume_ml': appointment_paint.volume_ml,
                            'appointment_id': appointment_paint.appointment_id,
                            'paint_id': appointment_paint.paint_id})
        db.session.execute('UPDATE Paint '
                           'SET left_ml = left_ml + :old_amount '
                           'WHERE id = :paint_id',
                           {'old_amount': old_amount,
                            'paint_id': appointment_paint.paint_id})
        db.session.execute('UPDATE Paint '
                           'SET left_ml = left_ml - :volume_ml '
                           'WHERE id = :paint_id',
                           {'volume_ml': appointment_paint.volume_ml,
                            'paint_id': appointment_paint.paint_id})
        assert_paint_enough(appointment_paint.paint_id)
        db.session.commit()
        return True, 'Успішно оновлено використання фарби'
    except IntegrityError:
        return False, 'Порушення цілісності використання фарби'
    except AssertionError as e:
        db.session.rollback()
        return False, e


def add_appointment_paint(appointment_paint: AppointmentPaint):
    if appointment_paint.volume_ml <= 0:
        return False, 'Кількість має бути більше нуля'
    try:
        assert_appointment_not_uses_paint(appointment_paint)
        db.session.execute('INSERT INTO Appointment_Paint (appointment_id, paint_id, volume_ml) '
                           'VALUES (:appointment_id, :paint_id, :volume_ml);',
                           {'appointment_id': appointment_paint.appointment_id,
                            'paint_id': appointment_paint.paint_id,
                            'volume_ml': appointment_paint.volume_ml})
        db.session.execute('UPDATE Paint '
                           'SET left_ml = left_ml - :volume_ml '
                           'WHERE id = :paint_id',
                           {'volume_ml': appointment_paint.volume_ml,
                            'paint_id': appointment_paint.paint_id})
        assert_paint_enough(appointment_paint.paint_id)
        db.session.commit()
        return True, 'Успішно додано використання фарби'
    except IntegrityError:
        return False, 'Порушення цілісності використання фарби'
    except AssertionError as e:
        db.session.rollback()
        return False, e


def delete_appointment_paint(appointment_id: int, paint_id: int):
    try:
        old_amount = db.session.execute('SELECT volume_ml '
                                        'FROM Appointment_Paint '
                                        'WHERE appointment_id = :appointment_id AND paint_id = :paint_id;',
                                        {'appointment_id': appointment_id,
                                         'paint_id': paint_id}).scalar()
        db.session.execute('DELETE '
                           'FROM Appointment_Paint '
                           'WHERE appointment_id = :appointment_id AND paint_id = :paint_id;',
                           {'appointment_id': appointment_id,
                            'paint_id': paint_id})
        db.session.execute('UPDATE Paint '
                           'SET left_ml = left_ml + :old_amount '
                           'WHERE id = :paint_id',
                           {'old_amount': old_amount,
                            'paint_id': paint_id})
        db.session.commit()
        return True, 'Успішно видалено використання фарби'
    except IntegrityError:
        return False, 'Порушення цілісності використання фарби'
