from sqlalchemy.exc import IntegrityError

from app import db
from app.models import PaintSupply
from app.api.asserts.asserts_paint import *


def get_supplies():
    return db.engine.execute('SELECT Paint.code AS paint_code, Paint.name AS paint_name, '
                             '       supply_date, amount, Paint_Supply.id AS id '
                             'FROM Paint INNER JOIN Paint_Supply '
                             '     ON Paint.id = Paint_Supply.paint_id '
                             'ORDER BY supply_date DESC').fetchall()


def get_supply(supply_id: int):
    return db.engine.execute('SELECT Paint_Supply.id, paint_id, supply_date, amount, '
                             '       code AS paint_code, '
                             '       name AS paint_name '
                             'FROM Paint_Supply INNER JOIN Paint ON paint_id = Paint.id '
                             'WHERE Paint_Supply.id = %s;',
                             supply_id).fetchone()


def update_supply(supply: PaintSupply):
    if supply.amount <= 0:
        return False, 'Поставка має бути більше нуля'
    if int(supply.paint_id) != get_supply(supply.id).paint_id:
        return False, 'Не можна змінювати фарбу у поставках'
    try:
        old_amount = db.session.execute('SELECT amount '
                                        'FROM Paint_Supply '
                                        'WHERE id = :id;',
                                        {'id': supply.id}).scalar()
        db.session.execute('UPDATE Paint_Supply '
                           'SET paint_id = :paint_id,'
                           '    amount = :amount,'
                           '    supply_date = :supply_date '
                           'WHERE id = :id;',
                           {'paint_id': supply.paint_id,
                            'amount': supply.amount,
                            'supply_date': supply.supply_date,
                            'id': supply.id})
        db.session.execute('UPDATE Paint '
                           'SET left_ml = left_ml - :old_amount '
                           'WHERE id = :paint_id',
                           {'old_amount': old_amount,
                            'paint_id': supply.paint_id})
        db.session.execute('UPDATE Paint '
                           'SET left_ml = left_ml + :amount '
                           'WHERE id = :paint_id',
                           {'amount': supply.amount,
                            'paint_id': supply.paint_id})
        assert_paint_enough(supply.paint_id)
        db.session.commit()
        return True, 'Успішно оновлено поставку'
    except IntegrityError:
        return False, 'Порушення цілісності поставок'
    except AssertionError as e:
        db.session.rollback()
        return False, e


def add_supply(supply: PaintSupply):
    if supply.amount <= 0:
        return False, 'Поставка має бути більше нуля'
    try:
        db.session.execute('INSERT INTO Paint_Supply (paint_id, amount, supply_date) '
                           'VALUES (:paint_id, :amount, :supply_date);',
                           {'paint_id': supply.paint_id,
                            'amount': supply.amount,
                            'supply_date': supply.supply_date})
        db.session.execute('UPDATE Paint '
                           'SET left_ml = left_ml + :amount '
                           'WHERE id = :paint_id',
                           {'amount': supply.amount,
                            'paint_id': supply.paint_id})
        db.session.commit()
        return True, 'Успішно додано поставку'
    except IntegrityError:
        return False, 'Порушення цілісності поставок'


def delete_supply(supply_id: int):
    try:
        old = db.session.execute('SELECT amount, paint_id '
                                 'FROM Paint_Supply '
                                 'WHERE id = :id;',
                                 {'id': supply_id}).fetchone()
        db.session.execute('DELETE '
                           'FROM Paint_Supply '
                           'WHERE id = :id',
                           {'id': supply_id})
        db.session.execute('UPDATE Paint '
                           'SET left_ml = left_ml - :amount '
                           'WHERE id = :id',
                           {'amount': old.amount,
                            'id': old.paint_id})
        assert_paint_enough(old.paint_id)
        db.session.commit()
        return True, 'Успішно видалено поставку'
    except IntegrityError:
        return False, 'Порушення цілісності поставок'
    except AssertionError as e:
        db.session.rollback()
        return False, e
