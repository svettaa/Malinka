import time

from sqlalchemy.exc import IntegrityError, DataError, OperationalError

from app import db, app
from app.db_api.utils import *
from app.db_api.asserts.appointments import *


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
                             'ORDER BY appoint_start DESC').fetchall()


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
                             '        master_id, client_id, procedure_id, '
                             '        uses_paints '
                             'FROM ((Appointment INNER JOIN Client M ON Appointment.master_id = M.id)'
                             '     INNER JOIN Client C ON Appointment.client_id = C.id)'
                             '     INNER JOIN Procedure ON Appointment.procedure_id = Procedure.id '
                             'WHERE Appointment.id = %s '
                             'ORDER BY appoint_start DESC;',
                             appointment_id).fetchone()


def get_master_date_appointments(master_id: int, date_obj: datetime):
    return db.session.execute('SELECT  C.surname AS client_surname, '
                              '        C.first_name AS client_first_name, '
                              '        Procedure.name AS procedure_name, '
                              '        status, appoint_start, appoint_end, '
                              '        preferences '
                              'FROM (Appointment INNER JOIN Client C ON Appointment.client_id = C.id)'
                              '     INNER JOIN Procedure ON Appointment.procedure_id = Procedure.id '
                              'WHERE master_id = :master_id AND Date(appoint_start) = :date_obj '
                              'ORDER BY appoint_start;',
                              {'master_id': master_id,
                               'date_obj': date_obj}).fetchall()


def get_client_future_appointments(client_id: int):
    return db.session.execute('SELECT  M.surname AS master_surname, '
                              '        M.first_name AS master_first_name, '
                              '        Procedure.name AS procedure_name, '
                              '        status, appoint_start, appoint_end, '
                              '        price_min, price_max, preferences, '
                              '        Appointment.id AS appointment_id '
                              'FROM ((Appointment INNER JOIN Client M ON Appointment.master_id = M.id)'
                              '     INNER JOIN Client C ON Appointment.client_id = C.id)'
                              '     INNER JOIN Procedure ON Appointment.procedure_id = Procedure.id '
                              'WHERE C.id = :client_id AND'
                              '      appoint_start > now() '
                              'ORDER BY appoint_start;',
                              {'client_id': client_id}).fetchall()


def get_client_past_appointments(client_id: int):
    return db.session.execute('SELECT  M.surname AS master_surname, '
                              '        M.first_name AS master_first_name, '
                              '        Procedure.name AS procedure_name, '
                              '        status, appoint_start, appoint_end, '
                              '        price, preferences, '
                              '        Appointment.id AS appointment_id '
                              'FROM ((Appointment INNER JOIN Client M ON Appointment.master_id = M.id)'
                              '     INNER JOIN Client C ON Appointment.client_id = C.id)'
                              '     INNER JOIN Procedure ON Appointment.procedure_id = Procedure.id '
                              'WHERE C.id = :client_id AND'
                              '      appoint_start <= now() '
                              'ORDER BY appoint_start;',
                              {'client_id': client_id}).fetchall()


def update_appointment(appointment: Appointment):
    if appointment.appoint_start >= appointment.appoint_end:
        return False, 'Початковий час має бути меньшим за кінцевий'
    if appointment.appoint_start.date() != appointment.appoint_end.date():
        return False, 'Запис має бути в межах одного дня'
    if appointment.appoint_start.time() < app.config['WORKING_DAY_START'] or \
            appointment.appoint_end.time() > app.config['WORKING_DAY_END']:
        return False, 'Запис має бути в межах робочого дня'
    original_appointment = get_appointment(appointment.id)
    if int(appointment.master_id) != original_appointment.master_id:
        return False, 'Не можна змінювати майстра у записі'
    if int(appointment.client_id) != original_appointment.client_id:
        return False, 'Не можна змінювати клієнта у записі'

    session = get_serializable_session()
    try:
        assert_appointment_is_in_nearest_future(appointment)
        assert_appointment_not_future_if_uses_paints(appointment, session)
        assert_appointment_master_does_procedure(appointment, session)
        assert_appointment_new_procedure_uses_paints(appointment, session)
        session.execute('UPDATE Appointment '
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
        assert_client_has_not_many_future_appointments(appointment, session)
        assert_appointment_is_hired(appointment, session)
        assert_appointment_is_relevant(appointment, session)
        assert_appointment_even_schedule_or_working(appointment, session)
        assert_appointment_master_no_vacation(appointment, session)
        assert_appointment_no_overlaps_client(appointment, session)
        assert_appointment_no_overlaps_master(appointment, session)
        session.commit()
        return True, 'Успішно оновлено запис'
    except IntegrityError:
        return False, 'Вже існує запис для даного клієнта чи майстра на цей час'
    except AssertionError as e:
        session.rollback()
        return False, e
    except DataError:
        session.rollback()
        return False, 'Занадто довге значення'
    except OperationalError:
        session.rollback()
        return update_appointment(appointment)
    finally:
        session.close()


def add_appointment(appointment: Appointment):
    if appointment.appoint_start >= appointment.appoint_end:
        return False, 'Початковий час має бути меньшим за кінцевий'
    if appointment.appoint_start.date() != appointment.appoint_end.date():
        return False, 'Запис має бути в межах одного дня'
    if appointment.appoint_start.time() < app.config['WORKING_DAY_START'] or \
            appointment.appoint_end.time() > app.config['WORKING_DAY_END']:
        return False, 'Запис має бути в межах робочого дня'
    if appointment.master_id == appointment.client_id:
        return False, 'Неможливо записати майстра до себе'

    session = get_serializable_session()
    try:
        assert_appointment_is_in_nearest_future(appointment)
        assert_appointment_master_does_procedure(appointment, session)
        session.execute('INSERT INTO Appointment (appoint_start, appoint_end, preferences,'
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
        assert_client_has_not_many_future_appointments(appointment, session)
        assert_appointment_is_hired(appointment, session)
        assert_appointment_is_relevant(appointment, session)
        assert_appointment_even_schedule_or_working(appointment, session)
        assert_appointment_master_no_vacation(appointment, session)
        assert_appointment_no_overlaps_client(appointment, session)
        assert_appointment_no_overlaps_master(appointment, session)
        session.commit()
        return True, 'Успішно додано запис'
    except IntegrityError:
        return False, 'Вже існує запис для даного клієнта чи майстра на цей час'
    except AssertionError as e:
        session.rollback()
        return False, e
    except DataError:
        session.rollback()
        return False, 'Занадто довге значення'
    except OperationalError:
        session.rollback()
        return add_appointment(appointment)
    finally:
        session.close()


def delete_appointment(appointment_id: int):
    try:
        db.engine.execute('DELETE '
                          'FROM Appointment '
                          'WHERE id = %s',
                          appointment_id)
        return True, 'Успішно видалено запис'
    except IntegrityError:
        return False, 'Запис використовує фарби'


def delete_appointment_if_future(appointment_id: int, user_id: int):
    try:
        appointment = get_appointment(appointment_id)
        if appointment is None:
            return False, 'Не існує такого запису'
        assert_appointment_client(appointment, user_id)
        assert_appointment_is_future(appointment_id)
        return delete_appointment(appointment_id)
    except AssertionError as e:
        db.session.rollback()
        return False, e
