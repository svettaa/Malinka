from app import db


def assert_user_has_favourite_master(client_id: int, master_id: int):
    if db.engine.execute('SELECT COUNT(*) '
                         'FROM Favourite_Master '
                         'WHERE client_id = %s AND master_id = %s;',
                         (client_id, master_id)).scalar() == 0:
        raise AssertionError('Майстра немає у списку улюблених')


def assert_user_has_favourite_procedure(client_id: int, procedure_id: int):
    if db.engine.execute('SELECT COUNT(*) '
                         'FROM Favourite_Procedure '
                         'WHERE client_id = %s AND procedure_id = %s;',
                         (client_id, procedure_id)).scalar() == 0:
        raise AssertionError('Процедури немає у списку улюблених')
