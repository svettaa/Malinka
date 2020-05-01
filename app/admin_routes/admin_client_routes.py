from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError, DataError

from app import app
from app.models import *
from app.message_codes import *
from app.forms import AdminClientForm


@app.route('/clients', methods=['GET'])
def clients_get():
    clients = db.engine.execute('SELECT id, surname, first_name, second_name, is_male, '
                                '       phone, email '
                                'FROM Client;').fetchall()

    return render_template('clients.html', clients=clients,
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/clients/<int:client_id>', methods=['GET'])
def edit_client_get(client_id):
    client = db.engine.execute('SELECT id, surname, first_name, second_name, is_male, '
                               '       phone, email '
                               'FROM Client '
                               'WHERE id = %s;',
                               client_id).fetchone()

    form = AdminClientForm(data=client)

    favourite_procedures = db.engine.execute('SELECT id, name '
                                             'FROM Favourite_Procedure INNER JOIN Procedure '
                                             '     ON procedure_id = id '
                                             'WHERE client_id = %s;',
                                             client_id).fetchall()

    favourite_masters = db.engine.execute('SELECT Master.id, surname, first_name, second_name, phone '
                                          'FROM (Favourite_Master INNER JOIN Master '
                                          '     ON master_id = id) INNER JOIN Client '
                                          '     ON Master.id = Client.id '
                                          'WHERE client_id = %s;',
                                          client_id).fetchall()

    return render_template('client.html', form=form,
                           favourite_procedures=favourite_procedures,
                           favourite_masters=favourite_masters,
                           action=url_for('edit_client_post', client_id=client_id))


@app.route('/clients/<int:client_id>', methods=['POST'])
def edit_client_post(client_id):
    form = AdminClientForm()

    favourite_procedures = db.engine.execute('SELECT id, name '
                                             'FROM Favourite_Procedure INNER JOIN Procedure '
                                             '     ON procedure_id = id '
                                             'WHERE client_id = %s;',
                                             client_id).fetchall()

    favourite_masters = db.engine.execute('SELECT Master.id, surname, first_name, second_name, phone '
                                          'FROM (Favourite_Master INNER JOIN Master '
                                          '     ON master_id = id) INNER JOIN Client '
                                          '     ON Master.id = Client.id '
                                          'WHERE client_id = %s;',
                                          client_id).fetchall()

    if not form.validate_on_submit():
        return render_template('client.html', form=form,
                               favourite_procedures=favourite_procedures,
                               favourite_masters=favourite_masters,
                               action=url_for('edit_client_post', client_id=client_id))

    client = Client(id=client_id)
    form.populate_obj(client)

    if client.second_name.strip() == '':
        client.second_name = None
    if client.email.strip() == '':
        client.email = None

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
    except IntegrityError:
        return render_template('client.html', form=form,
                               favourite_masters=favourite_masters,
                               favourite_procedures=favourite_procedures,
                               action=url_for('edit_client_post', client_id=client_id),
                               error=get_error_message(Error.USER_PHONE_EXISTS.value))

    return redirect(url_for('clients_get', success=Success.UPDATED_USER.value))


@app.route('/clients/new', methods=['GET'])
def new_client_get():
    form = AdminClientForm()

    return render_template('client.html', form=form,
                           action=url_for('new_client_post'))


@app.route('/clients/new', methods=['POST'])
def new_client_post():
    form = AdminClientForm()

    if not form.validate_on_submit():
        return render_template('client.html', form=form,
                               action=url_for('new_client_post'))

    client = Client()
    form.populate_obj(client)

    if client.second_name.strip() == '':
        client.second_name = None
    if client.email.strip() == '':
        client.email = None

    try:
        db.engine.execute('INSERT INTO Client (surname, first_name, second_name, is_male, '
                          '                    phone, email) '
                          'VALUES (%s, %s, %s, %s, %s, %s);',
                          (client.surname, client.first_name, client.second_name,
                           bool(client.is_male), client.phone, client.email))
    except IntegrityError:
        return render_template('client.html', form=form,
                               action=url_for('new_client_post'),
                               error=get_error_message(Error.USER_PHONE_EXISTS.value))

    return redirect(url_for('clients_get', success=Success.ADDED_USER.value))


@app.route('/clients/delete/<int:client_id>', methods=['GET'])
def delete_client_get(client_id):
    try:
        db.engine.execute('DELETE '
                          'FROM Client '
                          'WHERE id = %s',
                          client_id)
    except IntegrityError:
        return redirect(url_for('clients_get',
                                error=Error.USER_HAS_APPOINTMENTS.value))

    return redirect(url_for('clients_get', success=Success.DELETED_USER.value))
