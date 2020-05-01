from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError, DataError

from app import app
from app.models import *
from app.message_codes import *
from app.forms import AdminEditMasterForm, AdminNewMasterForm


@app.route('/masters', methods=['GET'])
def masters_get():
    masters = db.engine.execute('SELECT Master.id, surname, first_name, second_name, is_male, '
                                '       phone, email, even_schedule, is_hired '
                                'FROM Master INNER JOIN Client ON Master.id = Client.id;').fetchall()

    return render_template('masters.html', masters=masters,
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/masters/<int:master_id>', methods=['GET'])
def edit_master_get(master_id):
    master = db.engine.execute('SELECT Master.id, surname, first_name, second_name, phone, '
                               '       even_schedule, is_hired '
                               'FROM Client INNER JOIN Master ON Master.id = Client.id '
                               'WHERE Master.id = %s;',
                               master_id).fetchone()
    form = AdminEditMasterForm(data=master)

    favourite_clients_amount = db.engine.execute('SELECT COUNT(*) '
                                                 'FROM Favourite_Master '
                                                 'WHERE master_id = %s;',
                                                 master_id).scalar()

    procedures = db.engine.execute('SELECT * '
                                   'FROM Procedure;').fetchall()

    return render_template('master.html', master=master, form=form,
                           new_master=False,
                           favourite_clients_amount=favourite_clients_amount,
                           procedures=procedures,
                           action=url_for('edit_master_post', master_id=master_id))


@app.route('/masters/<int:master_id>', methods=['POST'])
def edit_master_post(master_id):
    form = AdminEditMasterForm()

    favourite_clients_amount = db.engine.execute('SELECT COUNT(*) '
                                                 'FROM Favourite_Master '
                                                 'WHERE master_id = %s;',
                                                 master_id).scalar()

    procedures = db.engine.execute('SELECT * '
                                   'FROM Procedure;').fetchall()

    master = db.engine.execute('SELECT Master.id, surname, first_name, second_name, phone, '
                               '       even_schedule, is_hired '
                               'FROM Client INNER JOIN Master ON Master.id = Client.id '
                               'WHERE Master.id = %s;',
                               master_id).fetchone()

    if not form.validate_on_submit():
        return render_template('master.html', master=master, form=form,
                               new_master=False,
                               favourite_clients_amount=favourite_clients_amount,
                               procedures=procedures,
                               action=url_for('edit_master_post', master_id=master_id))

    master = Master(id=master_id)
    form.populate_obj(master)

    db.engine.execute('UPDATE Master '
                      'SET even_schedule = %s,'
                      '    is_hired = %s '
                      'WHERE id = %s;',
                      (bool(master.even_schedule), bool(master.is_hired), master.id))

    return redirect(url_for('masters_get', success=Success.UPDATED_MASTER.value))


@app.route('/masters/new', methods=['GET'])
def new_master_get():
    users = db.engine.execute('SELECT id, surname, first_name, second_name, phone '
                              'FROM Client '
                              'WHERE NOT EXISTS (SELECT *'
                              '                  FROM Master '
                              '                  WHERE Master.id = Client.id) '
                              'ORDER BY surname, first_name, second_name, phone;').fetchall()
    form = AdminNewMasterForm()
    form.id.choices = [(user['id'], user['surname'] + ' ' + user['first_name'] + ', +38' + user['phone'])
                       for user in users]

    return render_template('master.html', form=form, new_master=True,
                           action=url_for('new_master_post'))


@app.route('/masters/new', methods=['POST'])
def new_master_post():
    form = AdminNewMasterForm()
    users = db.engine.execute('SELECT id, surname, first_name, second_name, phone '
                              'FROM Client '
                              'WHERE NOT EXISTS (SELECT *'
                              '                  FROM Master '
                              '                  WHERE Master.id = Client.id) '
                              'ORDER BY surname, first_name, second_name, phone;').fetchall()
    form.id.choices = [(user['id'], user['surname'] + user['first_name'] + ', +38' + user['phone']) for user in users]

    if not form.validate_on_submit():
        return render_template('master.html', form=form, new_master=True,
                               action=url_for('new_master_post'))

    master = Master()
    form.populate_obj(master)

    db.engine.execute('INSERT INTO Master (id, even_schedule, is_hired) '
                      'VALUES (%s, %s, %s);',
                      (master.id, bool(master.even_schedule), bool(master.is_hired)))

    return redirect(url_for('masters_get', success=Success.ADDED_MASTER.value))


@app.route('/masters/delete/<int:master_id>', methods=['GET'])
def delete_master_get(master_id):
    try:
        db.engine.execute('DELETE '
                          'FROM Master '
                          'WHERE id = %s',
                          master_id)
    except IntegrityError:
        return redirect(url_for('masters_get',
                                error=Error.MASTER_HAS_APPOINTMENTS.value))

    return redirect(url_for('masters_get', success=Success.DELETED_MASTER.value))
