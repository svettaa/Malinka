from sqlalchemy.exc import IntegrityError

from app import db
from app.models import PaintSupply


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
    if int(supply.paint_id) != get_supply(supply.id).paint_id:
        return False, 'Не можна змінювати фарбу у поставках'
    try:
        old_amount = db.engine.execute('SELECT amount '
                                       'FROM Paint_Supply '
                                       'WHERE id = %s;',
                                       supply.id).fetchone()['amount']
        db.engine.execute('UPDATE Paint_Supply '
                          'SET paint_id = %s,'
                          '    amount = %s,'
                          '    supply_date = %s '
                          'WHERE id = %s;',
                          (supply.paint_id, supply.amount,
                           supply.supply_date, supply.id))
        db.engine.execute('UPDATE Paint '
                          'SET left_ml = left_ml - %s '
                          'WHERE id = %s',
                          (old_amount, supply.paint_id))
        db.engine.execute('UPDATE Paint '
                          'SET left_ml = left_ml + %s '
                          'WHERE id = %s',
                          (supply.amount, supply.paint_id))
        return True, 'Успішно оновлено поставку'
    except IntegrityError:
        return False, 'Порушення цілісності поставок'


def add_supply(supply: PaintSupply):
    try:
        db.engine.execute('INSERT INTO Paint_Supply (paint_id, amount, supply_date) '
                          'VALUES (%s, %s, %s);',
                          (supply.paint_id, supply.amount, supply.supply_date))
        db.engine.execute('UPDATE Paint '
                          'SET left_ml = left_ml + %s '
                          'WHERE id = %s',
                          (supply.amount, supply.paint_id))
        return True, 'Успішно додано поставку'
    except IntegrityError:
        return False, 'Порушення цілісності поставок'


def delete_supply(supply_id: int):
    try:
        old = db.engine.execute('SELECT amount, paint_id '
                                'FROM Paint_Supply '
                                'WHERE id = %s;',
                                supply_id).fetchone()
        db.engine.execute('DELETE '
                          'FROM Paint_Supply '
                          'WHERE id = %s',
                          supply_id)
        db.engine.execute('UPDATE Paint '
                          'SET left_ml = left_ml - %s '
                          'WHERE id = %s',
                          (old['amount'], old['paint_id']))
        return True, 'Успішно видалено поставку'
    except IntegrityError:
        return False, 'Порушення цілісності поставок'
