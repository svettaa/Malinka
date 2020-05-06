from sqlalchemy.exc import IntegrityError

from app import db
from app.api.asserts.asserts_appointment import *


def get_appointments():
    return db.engine.execute('SELECT  M.surname AS master_surname, '
                             '        M.first_name AS master_first_name, '
                             '        C.surname AS client_surname, '
                             '        C.first_name AS client_first_name, '
                             '        Procedure.name AS procedure_name, '
                             '        status, appoint_start, appoint_end, '
                             '        price, preferences, Appointment.id '
                             'FROM ((Appointment INNER JOIN Client M ON Appointment.master_id = M.id)'
                             '     INNER JOIN Client C ON Appointment.client_id = C.id)'
                             '     INNER JOIN Procedure ON Appointment.procedure_id = Procedure.id '
                             'ORDER BY appoint_start').fetchall()


def get_appointment(appointment_id: int):
    return db.engine.execute('SELECT  M.surname AS master_surname, '
                             '        M.first_name AS master_first_name, '
                             '        M.id AS master_id, '
                             '        C.surname AS client_surname, '
                             '        C.first_name AS client_first_name, '
                             '        C.phone AS client_phone, '
                             '        C.id AS client_id, '
                             '        Procedure.name AS procedure_name, '
                             '        Procedure.id AS procedure_id, '
                             '        status, appoint_start, appoint_end, '
                             '        price, preferences, Appointment.id,'
                             '        master_id, client_id, procedure_id '
                             'FROM ((Appointment INNER JOIN Client M ON Appointment.master_id = M.id)'
                             '     INNER JOIN Client C ON Appointment.client_id = C.id)'
                             '     INNER JOIN Procedure ON Appointment.procedure_id = Procedure.id '
                             'WHERE Appointment.id = %s '
                             'ORDER BY appoint_start;',
                             appointment_id).fetchone()


def update_appointment(appointment: Appointment):
    original_appointment = get_appointment(appointment.id)
    if int(appointment.master_id) != original_appointment.master_id:
        return False, 'Не можна змінювати майстра у записі'
    if int(appointment.client_id) != original_appointment.client_id:
        return False, 'Не можна змінювати клієнта у записі'
    try:
        db.session.execute('UPDATE Appointment '
                           'SET appoint_start = :appoint_start, '
                           '    appoint_end = :appoint_end, '
                           '    preferences = :preferences,'
                           '    status = :status, '
                           '    price = :price, '
                           '    client_id = :client_id, '
                           '    master_id = :master_id, '
                           '    procedure_id = :procedure_id '
                           'WHERE id = :id;',
                           {'appoint_start': appointment.appoint_start,
                            'appoint_end': appointment.appoint_end,
                            'preferences': appointment.preferences,
                            'status': appointment.status,
                            'price': appointment.price,
                            'client_id': appointment.client_id,
                            'master_id': appointment.master_id,
                            'procedure_id': appointment.procedure_id,
                            'id': appointment.id})
        assert_appointment_is_hired(appointment)
        db.session.commit()
        return True, 'Успішно оновлено запис'
    except IntegrityError:
        return False, ''
    except AssertionError as e:
        db.session.rollback()
        return False, e


def add_appointment(appointment: Appointment):
    if appointment.master_id == appointment.client_id:
        return False, 'Неможливо записати майстра до себе'
    try:
        db.session.execute('INSERT INTO Appointment (appoint_start, appoint_end, preferences,'
                           '                         status, price, client_id, master_id, procedure_id) '
                           'VALUES (:appoint_start, :appoint_end, :preferences,'
                           '        :status, :price, :client_id, :master_id, :procedure_id);',
                           {'appoint_start': appointment.appoint_start,
                            'appoint_end': appointment.appoint_end,
                            'preferences': appointment.preferences,
                            'status': appointment.status,
                            'price': appointment.price,
                            'client_id': appointment.client_id,
                            'master_id': appointment.master_id,
                            'procedure_id': appointment.procedure_id})
        assert_appointment_is_hired(appointment)
        db.session.commit()
        return True, 'Успішно додано запис'
    except IntegrityError:
        return False, ''
    except AssertionError as e:
        db.session.rollback()
        return False, e


def delete_appointment(appointment_id: int):
    try:
        db.engine.execute('DELETE '
                          'FROM Appointment '
                          'WHERE id = %s',
                          appointment_id)
        return True, 'Успішно видалено запис'
    except IntegrityError:
        return False, 'Запис використовує фарби'
