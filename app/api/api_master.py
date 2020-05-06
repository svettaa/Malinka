from sqlalchemy.exc import IntegrityError

from app import db
from app.api.asserts.asserts_master import *


def get_masters():
    return db.engine.execute('SELECT Master.id, surname, first_name, second_name, is_male, '
                             '       phone, email, even_schedule, is_hired '
                             'FROM Master INNER JOIN Client ON Master.id = Client.id;').fetchall()


def get_master(master_id: int):
    return db.engine.execute('SELECT Master.id, surname, first_name, second_name, is_male, '
                             '       phone, email, even_schedule, is_hired '
                             'FROM Client INNER JOIN Master ON Master.id = Client.id '
                             'WHERE Master.id = %s;',
                             master_id).fetchone()


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
    try:
        db.session.execute('UPDATE Master '
                           'SET even_schedule =:even_schedule,'
                           '    is_hired = :is_hired '
                           'WHERE id = :id;',
                           {'even_schedule': bool(master.even_schedule),
                            'is_hired': bool(master.is_hired),
                            'id': master.id})
        assert_master_is_hired(master)
        assert_master_even_schedule_or_working(master)
        db.session.commit()
        return True, 'Успішно оновлено майстра'
    except IntegrityError:
        return False, ''
    except AssertionError as e:
        db.session.rollback()
        return False, e


def update_master_procedures(master_id: int, procedures):
    # delete old
    try:
        db.engine.execute('DELETE FROM Master_Procedure '
                          'WHERE master_id = %s;',
                          master_id)
    except IntegrityError:
        return False, ''

    # insert new
    for procedure in procedures:
        if procedure.duration.data is not None:
            try:
                db.engine.execute('INSERT INTO Master_Procedure '
                                  '            (master_id, procedure_id, duration) '
                                  'VALUES (%s, %s, %s);',
                                  (master_id, procedure.procedure_id.data, procedure.duration.data))
            except IntegrityError:
                return False, ''
    return True, 'Успішно змінено процедури майстра'


def add_master(master: Master):
    try:
        db.engine.execute('INSERT INTO Master (id, even_schedule, is_hired) '
                          'VALUES (%s, %s, %s);',
                          (master.id, bool(master.even_schedule), bool(master.is_hired)))
        return True, 'Успішно додано майстра'
    except IntegrityError:
        return False, ''


def delete_master(master_id: int):
    try:
        db.engine.execute('DELETE '
                          'FROM Master '
                          'WHERE id = %s',
                          master_id)
        return True, 'Успішно видалено майстра'
    except IntegrityError:
        return False, 'Майстер міститься у записах, улюблених, змінах графіку, або вміє робити процедури'
