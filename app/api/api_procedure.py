from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Procedure


def get_procedures():
    return db.engine.execute('SELECT Procedure.id, price_min, price_max, info, '
                             '       Procedure.name AS procedure_name, '
                             '       Category.name AS category_name '
                             'FROM Procedure INNER JOIN Category '
                             '     ON Procedure.category_id = Category.id '
                             'ORDER BY Category.id').fetchall()


def get_procedure(procedure_id: int):
    return db.engine.execute('SELECT id, name, category_id, price_min, price_max, info '
                             'FROM Procedure '
                             'WHERE id = %s;',
                             procedure_id).fetchone()


def get_procedure_favourite_clients_amount(procedure_id: int):
    return db.engine.execute('SELECT COUNT(*) '
                             'FROM Favourite_Procedure '
                             'WHERE procedure_id = %s;',
                             procedure_id).scalar()


def update_procedure(procedure: Procedure):
    try:
        db.engine.execute('UPDATE Procedure '
                          'SET category_id = %s,'
                          '    name = %s,'
                          '    price_min = %s,'
                          '    price_max = %s, '
                          '    info = %s '
                          'WHERE id = %s;',
                          (procedure.category_id, procedure.name, procedure.price_min,
                           procedure.price_max, procedure.info, procedure.id))
        return True, 'Успішно оновлено процедуру'
    except IntegrityError:
        return False, 'Процедура з такою назвою вже існує або максимальна ціна менша за мінімальну'


def add_procedure(procedure: Procedure):
    try:
        db.engine.execute('INSERT INTO Procedure (category_id, name, price_min, price_max, info) '
                          'VALUES (%s, %s, %s, %s, %s);',
                          (procedure.category_id, procedure.name, procedure.price_min,
                           procedure.price_max, procedure.info))
        return True, 'Успішно додано процедуру'
    except IntegrityError:
        return False, 'Процедура з такою назвою вже існує або максимальна ціна менша за мінімальну'


def delete_procedure(procedure_id: int):
    try:
        db.engine.execute('DELETE '
                          'FROM Procedure '
                          'WHERE id = %s',
                          procedure_id)
        return True, 'Успішно видалено процедуру'
    except IntegrityError:
        return False, 'Процедура міститься у записах або є у списку улюблених'
