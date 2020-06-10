from sqlalchemy.exc import IntegrityError, DataError, OperationalError

from app import db
from app.db_api.utils import *
from app.models import Procedure
from app.db_api.asserts.procedures import *


def get_procedures():
    return db.engine.execute('SELECT Procedure.id, price_min, price_max, info, uses_paints, '
                             '       Procedure.name AS procedure_name, '
                             '       Category.name AS category_name, '
                             '       is_relevant '
                             'FROM Procedure INNER JOIN Category '
                             '     ON Procedure.category_id = Category.id '
                             'ORDER BY Category.id').fetchall()


def get_relevant_procedures_short():
    return db.engine.execute('SELECT Procedure.id, price_min, price_max, info, '
                             '       Procedure.name AS procedure_name, '
                             '       Category.name AS category_name '
                             'FROM Procedure INNER JOIN Category '
                             '     ON Procedure.category_id = Category.id '
                             'WHERE is_relevant = True '
                             'ORDER BY Category.id').fetchall()


def get_procedure(procedure_id: int):
    return db.engine.execute('SELECT id, name, category_id, price_min, price_max, info, uses_paints, '
                             '       is_relevant '
                             'FROM Procedure '
                             'WHERE id = %s;',
                             procedure_id).fetchone()


def get_procedure_favourite_clients_amount(procedure_id: int):
    return db.engine.execute('SELECT COUNT(*) '
                             'FROM Favourite_Procedure '
                             'WHERE procedure_id = %s;',
                             procedure_id).scalar()


def update_procedure(procedure: Procedure):
    if procedure.price_max is not None and \
            procedure.price_max <= procedure.price_min:
        return False, 'Мінімальна ціна має бути меншою за максимальну'

    session = get_serializable_session()
    try:
        session.execute('UPDATE Procedure '
                        'SET category_id = :category_id,'
                        '    name = :name,'
                        '    price_min = :price_min,'
                        '    price_max = :price_max, '
                        '    info = :info, '
                        '    uses_paints = :uses_paints, '
                        '    is_relevant = :is_relevant '
                        'WHERE id = :id;',
                        {'category_id': procedure.category_id,
                         'name': procedure.name,
                         'price_min': procedure.price_min,
                         'price_max': procedure.price_max,
                         'info': procedure.info,
                         'uses_paints': procedure.uses_paints,
                         'is_relevant': procedure.is_relevant,
                         'id': procedure.id})
        assert_procedure_is_relevant(procedure, session)
        assert_procedure_uses_paints(procedure, session)
        session.commit()
        return True, 'Успішно оновлено процедуру'
    except IntegrityError:
        session.rollback()
        return False, 'Процедура з такою назвою вже існує'
    except AssertionError as e:
        session.rollback()
        return False, e
    except OperationalError:
        session.rollback()
        return update_procedure(procedure)
    except DataError:
        session.rollback()
        return False, 'Занадто довге значення'
    finally:
        session.close()


def add_procedure(procedure: Procedure):
    if procedure.price_max is not None and \
            procedure.price_max <= procedure.price_min:
        return False, 'Мінімальна ціна має бути меншою за максимальну'
    try:
        db.engine.execute('INSERT INTO Procedure '
                          '      (category_id, name, price_min, price_max, info, uses_paints, is_relevant) '
                          'VALUES (%s, %s, %s, %s, %s, %s, %s);',
                          (procedure.category_id, procedure.name, procedure.price_min,
                           procedure.price_max, procedure.info, procedure.uses_paints,
                           procedure.is_relevant))
        return True, 'Успішно додано процедуру'
    except IntegrityError:
        return False, 'Процедура з такою назвою вже існує'
    except DataError:
        db.session.rollback()
        return False, 'Занадто довге значення'


def delete_procedure(procedure_id: int):
    try:
        db.engine.execute('DELETE '
                          'FROM Procedure '
                          'WHERE id = %s',
                          procedure_id)
        return True, 'Успішно видалено процедуру'
    except IntegrityError:
        return False, 'Процедура міститься у записах, списку улюблених або вміннях майстра'
