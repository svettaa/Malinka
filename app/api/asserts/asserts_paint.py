from app import db


def assert_paint_enough(paint_id: int):
    if db.session.execute('SELECT left_ml '
                          'FROM Paint '
                          'WHERE id = :paint_id;',
                          {'paint_id': paint_id}).scalar() < 0:
        raise AssertionError('Неможливо виконати операцію, недостатньо фарби')
