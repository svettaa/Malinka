from sqlalchemy.exc import IntegrityError, DataError

from app import db
from app.models import Client


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
