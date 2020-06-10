from datetime import datetime

from sqlalchemy.exc import IntegrityError, OperationalError

from app import db
from app.db_api.utils import *
from app.db_api.asserts.masters import *


def get_masters():
    return db.engine.execute('SELECT Master.id, surname, first_name, second_name, is_male, '
                             '       phone, email, even_schedule, is_hired '
                             'FROM Master INNER JOIN Client ON Master.id = Client.id;').fetchall()


def get_master(master_id: int):
    return db.engine.execute('SELECT Master.id, surname, first_name, second_name, is_male, '
                             '       phone, email, even_schedule, is_hired, info '
                             'FROM Client INNER JOIN Master ON Master.id = Client.id '
                             'WHERE Master.id = %s;',
                             master_id).fetchone()


def get_master_procedure_duration(master_id: int, procedure_id: int):
    return db.engine.execute('SELECT duration '
                             'FROM Master_Procedure '
                             'WHERE master_id = %s AND procedure_id = %s;',
                             (master_id, procedure_id)).scalar()


def get_masters_working(date: datetime):
    day = date.day
    even_day = (day % 2 == 0)

    return db.session.execute('SELECT Master.id, surname, first_name, second_name, is_male, '
                              '       phone, email, even_schedule, is_hired '
                              'FROM Master INNER JOIN Client ON Master.id = Client.id '
                              'WHERE is_hired = True AND '
                              '       (even_schedule = :even_day '
                              '        OR EXISTS (SELECT * '
                              '                  FROM Schedule_Change '
                              '                  WHERE master_id = Master.id AND is_working = True AND '
                              '                        :date BETWEEN Date(change_start) AND DATE(change_end)) '
                              '        ) '
                              '      OR '
                              '          (:date <= Date(now()) AND'
                              '          EXISTS (SELECT * '
                              '                  FROM Appointment '
                              '                  WHERE master_id = Master.id AND '
                              '                        Date(appoint_start) = :date));',
                              {'even_day': even_day, 'date': date}).fetchall()


def get_masters_working_do_procedure_client_view(date: datetime, procedure_id: str):
    day = date.day
    even_day = (day % 2 == 0)

    return db.session.execute('SELECT Master.id, surname, first_name, duration '
                              'FROM (Master INNER JOIN Client ON Master.id = Client.id) '
                              '      INNER JOIN Master_Procedure ON Master.id = master_id '
                              'WHERE '
                              '     procedure_id = :procedure_id AND '
                              '     is_hired = True AND '
                              '     ('
                              '      even_schedule = :even_day '
                              '      OR EXISTS (SELECT * '
                              '                 FROM Schedule_Change '
                              '                 WHERE master_id = Master.id AND is_working = True AND '
                              '                       :date BETWEEN Date(change_start) AND DATE(change_end))  '
                              '      );',
                              {'even_day': even_day,
                               'date': date,
                               'procedure_id': procedure_id}).fetchall()


def get_master_date_vacations(master_id: int, date_obj: datetime):
    return db.engine.execute('SELECT change_start, change_end '
                             'FROM Schedule_Change '
                             'WHERE master_id = %s AND is_working = False AND '
                             '      %s BETWEEN Date(change_start) AND DATE(change_end);',
                             (master_id, date_obj)).fetchall()


def get_master_date_overworks(master_id: int, date_obj: datetime):
    return db.engine.execute('SELECT change_start, change_end '
                             'FROM Schedule_Change '
                             'WHERE master_id = %s AND is_working = True AND '
                             '      %s BETWEEN Date(change_start) AND DATE(change_end) '
                             'ORDER BY change_start;',
                             (master_id, date_obj)).fetchall()


def get_all_procedures_join_master(master_id: int):
    return db.engine.execute('SELECT  duration, '
                             '        Procedure.name AS procedure_name, '
                             '        Procedure.id AS procedure_id, '
                             '        Category.name AS category_name '
                             'FROM ((Procedure INNER JOIN Category '
                             '       ON Category.id = category_id) '
                             '            CROSS JOIN Master) '
                             '            LEFT JOIN Master_Procedure '
                             '                     ON Procedure.id = procedure_id AND'
                             '                          Master.id = master_id '
                             'WHERE Master.id = %s '
                             'ORDER BY category_id;',
                             master_id).fetchall()


def get_master_favourite_clients_amount(master_id: int):
    return db.engine.execute('SELECT COUNT(*) '
                             'FROM Favourite_Master '
                             'WHERE master_id = %s;',
                             master_id).scalar()


def update_master(master: Master):
    session = get_serializable_session()
    try:
        session.execute('UPDATE Master '
                        'SET even_schedule =:even_schedule,'
                        '    is_hired = :is_hired, '
                        '    info = :info '
                        'WHERE id = :id;',
                        {'even_schedule': bool(master.even_schedule),
                         'is_hired': bool(master.is_hired),
                         'info': master.info,
                         'id': master.id})
        assert_master_is_hired(master, session)
        assert_master_even_schedule_or_working(master, session)
        session.commit()
        return True, 'Успішно оновлено майстра'
    except IntegrityError:
        session.rollback()
        return False, ''
    except AssertionError as e:
        session.rollback()
        return False, e
    except OperationalError:
        session.rollback()
        return update_master(master)
    finally:
        session.close()


def update_master_procedures(master_id: int, procedures):
    for procedure in procedures:
        if procedure['duration'] is not None and procedure['duration'] <= 0:
            return False, 'Тривалість виконання має бути більше нуля'

    session = get_serializable_session()
    try:
        # delete old
        session.execute('DELETE FROM Master_Procedure '
                        'WHERE master_id = :master_id;',
                        {'master_id': master_id})

        # insert new
        for procedure in procedures:
            if procedure['duration'] is not None:
                session.execute('INSERT INTO Master_Procedure '
                                '            (master_id, procedure_id, duration) '
                                'VALUES (:master_id, :procedure_id, :duration);',
                                {'master_id': master_id,
                                 'procedure_id': procedure['procedure_id'],
                                 'duration': procedure['duration']})

        assert_master_procedures(get_master(master_id), session)
        session.commit()
        return True, 'Успішно змінено процедури майстра'
    except IntegrityError:
        session.rollback()
        return False, 'Некоректний номер процедури'
    except AssertionError as e:
        session.rollback()
        return False, e
    except OperationalError:
        session.rollback()
        return update_master_procedures(master_id, procedures)
    finally:
        session.close()


def add_master(master: Master):
    try:
        db.engine.execute('INSERT INTO Master (id, even_schedule, is_hired, info) '
                          'VALUES (%s, %s, %s, %s);',
                          (master.id, bool(master.even_schedule), bool(master.is_hired), master.info))
        return True, 'Успішно додано майстра'
    except IntegrityError:
        return False, 'Вже існує такий майстер'


def delete_master(master_id: int):
    try:
        db.engine.execute('DELETE '
                          'FROM Master '
                          'WHERE id = %s',
                          master_id)
        return True, 'Успішно видалено майстра'
    except IntegrityError:
        return False, 'Майстер міститься у записах, улюблених, змінах графіку, або вміє робити процедури'
