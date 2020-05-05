from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Appointment


def get_appointments():
    return db.engine.execute('SELECT  M.surname AS master_surname, '
                             '        M.first_name AS master_first_name, '
                             '        C.surname AS client_surname, '
                             '        C.first_name AS client_first_name, '
                             '        Procedure.name AS procedure_name, '
                             '        status, appoint_date, start_time, end_time, '
                             '        price, preferences, Appointment.id '
                             'FROM ((Appointment INNER JOIN Client M ON Appointment.master_id = M.id)'
                             '     INNER JOIN Client C ON Appointment.client_id = C.id)'
                             '     INNER JOIN Procedure ON Appointment.procedure_id = Procedure.id '
                             'ORDER BY appoint_date').fetchall()


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
                             '        status, appoint_date, start_time, end_time, '
                             '        price, preferences, Appointment.id,'
                             '        master_id, client_id, procedure_id '
                             'FROM ((Appointment INNER JOIN Client M ON Appointment.master_id = M.id)'
                             '     INNER JOIN Client C ON Appointment.client_id = C.id)'
                             '     INNER JOIN Procedure ON Appointment.procedure_id = Procedure.id '
                             'WHERE Appointment.id = %s '
                             'ORDER BY appoint_date;',
                             appointment_id).fetchone()


def update_appointment(appointment: Appointment):
    original_appointment = get_appointment(appointment.id)
    if int(appointment.master_id) != original_appointment.master_id:
        return False, 'Не можна змінювати майстра у записі'
    if int(appointment.client_id) != original_appointment.client_id:
        return False, 'Не можна змінювати клієнта у записі'
    try:
        db.engine.execute('UPDATE Appointment '
                          'SET appoint_date = %s, '
                          '    start_time = %s, '
                          '    end_time = %s, '
                          '    preferences = %s,'
                          '    status = %s, '
                          '    price = %s, '
                          '    client_id = %s, '
                          '    master_id = %s, '
                          '    procedure_id = %s '
                          'WHERE id = %s;',
                          (appointment.appoint_date, appointment.start_time, appointment.end_time,
                           appointment.preferences, appointment.status, appointment.price,
                           appointment.client_id, appointment.master_id, appointment.procedure_id,
                           appointment.id))
        return True, 'Успішно оновлено запис'
    except IntegrityError:
        return False, ''


def add_appointment(appointment: Appointment):
    try:
        db.engine.execute('INSERT INTO Appointment (appoint_date, start_time, end_time, preferences,'
                          '                         status, price, client_id, master_id, procedure_id) '
                          'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);',
                          (appointment.appoint_date, appointment.start_time, appointment.end_time,
                           appointment.preferences, appointment.status, appointment.price,
                           appointment.client_id, appointment.master_id, appointment.procedure_id))
        return True, 'Успішно додано запис'
    except IntegrityError:
        return False, ''


def delete_appointment(appointment_id: int):
    try:
        db.engine.execute('DELETE '
                          'FROM Appointment '
                          'WHERE id = %s',
                          appointment_id)
        return True, 'Успішно видалено запис'
    except IntegrityError:
        return False, 'Запис використовує фарби'
