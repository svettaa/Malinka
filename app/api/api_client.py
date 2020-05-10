from sqlalchemy.exc import IntegrityError, DataError

from app import db
from app.models import Client
from app.api.asserts.asserts_client import *


def get_clients():
    return db.engine.execute('SELECT id, surname, first_name, second_name, is_male, '
                             '       phone, email '
                             'FROM Client;').fetchall()


def get_clients_no_masters():
    return db.engine.execute('SELECT id, surname, first_name, second_name, is_male, '
                             '       phone, email '
                             'FROM Client '
                             'WHERE NOT EXISTS (SELECT *'
                             '                  FROM Master '
                             '                  WHERE Master.id = Client.id);').fetchall()


def get_client(client_id: int):
    return db.engine.execute('SELECT id, surname, first_name, second_name, is_male, '
                             '       phone, email '
                             'FROM Client '
                             'WHERE id = %s;',
                             client_id).fetchone()


def get_client_favourite_masters(client_id: int):
    return db.engine.execute('SELECT Master.id, surname, first_name, second_name, phone '
                             'FROM (Favourite_Master INNER JOIN Master '
                             '     ON master_id = id) INNER JOIN Client '
                             '     ON Master.id = Client.id '
                             'WHERE client_id = %s;',
                             client_id).fetchall()


def get_client_favourite_procedures(client_id: int):
    return db.engine.execute('SELECT id, name '
                             'FROM Favourite_Procedure INNER JOIN Procedure '
                             '     ON procedure_id = id '
                             'WHERE client_id = %s;',
                             client_id).fetchall()


def update_client(client: Client):
    try:
        db.engine.execute('UPDATE Client '
                          'SET surname = %s,'
                          '    first_name = %s, '
                          '    second_name = %s, '
                          '    is_male = %s, '
                          '    phone = %s, '
                          '    email = %s '
                          'WHERE id = %s;',
                          (client.surname, client.first_name, client.second_name,
                           bool(client.is_male), client.phone, client.email, client.id))
        return True, 'Успішно оновлено користувача'
    except IntegrityError:
        return False, 'Користувач з таким телефоном вже існує'
    except DataError:
        db.session.rollback()
        return False, 'Занадто довге значення'


def add_client(client: Client):
    try:
        db.engine.execute('INSERT INTO Client (surname, first_name, second_name, is_male, '
                          '                    phone, email) '
                          'VALUES (%s, %s, %s, %s, %s, %s);',
                          (client.surname, client.first_name, client.second_name,
                           bool(client.is_male), client.phone, client.email))
        return True, 'Успішно додано клієнта'
    except IntegrityError:
        return False, 'Користувач з таким телефоном вже існує'
    except DataError:
        db.session.rollback()
        return False, 'Занадто довге значення'


def add_client_favourite_master(client_id: int, master_id: int):
    try:
        assert_user_has_NOT_favourite_master(client_id, master_id)
        db.engine.execute('INSERT INTO Favourite_Master (client_id, master_id) '
                          'VALUES (%s, %s);',
                          (client_id, master_id))
        return True, 'Успішно додано улюбленого майстра'
    except AssertionError as e:
        db.session.rollback()
        return False, e


def add_client_favourite_procedure(client_id: int, procedure_id: int):
    try:
        assert_user_has_NOT_favourite_procedure(client_id, procedure_id)
        db.engine.execute('INSERT INTO Favourite_Procedure (client_id, procedure_id) '
                          'VALUES (%s, %s);',
                          (client_id, procedure_id))
        return True, 'Успішно додано улюблену процедуру'
    except AssertionError as e:
        db.session.rollback()
        return False, e


def delete_client(client_id: int):
    try:
        db.engine.execute('DELETE '
                          'FROM Client '
                          'WHERE id = %s',
                          client_id)
        return True, 'Успішно видалено клієнта'
    except IntegrityError:
        return False, 'Неможливо видалити користувача, що має улюблених майстрів чи процедур, міститься в записах ' \
                      'або є майстром'


def delete_client_favourite_master(client_id: int, master_id: int):
    try:
        assert_user_has_favourite_master(client_id, master_id)
        db.engine.execute('DELETE '
                          'FROM Favourite_Master '
                          'WHERE client_id = %s AND master_id = %s;',
                          (client_id, master_id))
        return True, 'Успішно видалено улюбленого майстра'
    except AssertionError as e:
        db.session.rollback()
        return False, e


def delete_client_favourite_procedure(client_id: int, procedure_id: int):
    try:
        assert_user_has_favourite_procedure(client_id, procedure_id)
        db.engine.execute('DELETE '
                          'FROM Favourite_Procedure '
                          'WHERE client_id = %s AND procedure_id = %s;',
                          (client_id, procedure_id))
        return True, 'Успішно видалено улюблену процедуру'
    except AssertionError as e:
        db.session.rollback()
        return False, e
