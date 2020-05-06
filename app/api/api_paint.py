from sqlalchemy.exc import IntegrityError, DataError

from app import db
from app.models import Paint


def get_paints():
    return db.engine.execute('SELECT id, code, name, left_ml '
                             'FROM Paint;').fetchall()


def get_paint(paint_id: int):
    return db.engine.execute('SELECT id, code, name, left_ml '
                             'FROM Paint '
                             'WHERE id = %s;',
                             paint_id).fetchone()


def update_paint(paint: Paint):
    try:
        db.engine.execute('UPDATE Paint '
                          'SET code = %s,'
                          '    name = %s '
                          'WHERE id = %s;',
                          (paint.code, paint.name, paint.id))
        return True, 'Успішно оновлено фарбу'
    except IntegrityError:
        return False, 'Фарба з таким кодом вже існує'
    except DataError:
        db.session.rollback()
        return False, 'Занадто довге значення'


def add_paint(paint: Paint):
    try:
        db.engine.execute('INSERT INTO Paint (code, name, left_ml) '
                          'VALUES (%s, %s, %s);',
                          (paint.code, paint.name, 0))
        return True, 'Успішно додано фарбу'
    except IntegrityError:
        return False, 'Фарба з таким кодом вже існує'
    except DataError:
        db.session.rollback()
        return False, 'Занадто довге значення'


def delete_paint(paint_id: int):
    try:
        db.engine.execute('DELETE '
                          'FROM Paint '
                          'WHERE id = %s',
                          paint_id)
        return True, 'Успішно видалено фарбу'
    except IntegrityError:
        return False, 'Фарба міститься у записах або поставках'
