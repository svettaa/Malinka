from sqlalchemy.exc import IntegrityError, DataError

from app import db
from app.models import Category


def get_categories():
    return db.engine.execute('SELECT id, name '
                             'FROM Category '
                             'ORDER BY id;').fetchall()


def get_category(category_id: int):
    return db.engine.execute('SELECT id, name '
                             'FROM Category '
                             'WHERE id = %s;',
                             category_id).fetchone()


def update_category(category: Category):
    try:
        db.engine.execute('UPDATE Category '
                          'SET name = %s '
                          'WHERE id = %s;',
                          (category.name, category.id))
        return True, 'Успішно оновлено категорію'
    except IntegrityError:
        return False, 'Категорія з такою назвою вже існує'
    except DataError:
        db.session.rollback()
        return False, 'Занадто довге значення'


def add_category(category:Category):
    try:
        db.engine.execute('INSERT INTO Category (name) '
                          'VALUES (%s);',
                          category.name)
        return True, 'Успішно додано категорію'
    except IntegrityError:
        return False, 'Категорія з такою назвою вже існує'
    except DataError:
        db.session.rollback()
        return False, 'Занадто довге значення'


def delete_category(category_id: int):
    try:
        db.engine.execute('DELETE '
                          'FROM Category '
                          'WHERE id = %s',
                          category_id)
        return True, 'Успішно видалено категорію'
    except IntegrityError:
        return False, 'Категорія містить процедури'
