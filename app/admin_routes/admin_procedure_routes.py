from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError, DataError

from app import app
from app.models import *
from app.message_codes import *
from app.forms import AdminProcedureForm


@app.route('/procedures')
def procedures_get():
    procedures = db.engine.execute('SELECT Procedure.id, price_min, price_max, info, '
                                   '       Procedure.name AS procedure_name, '
                                   '       Category.name AS category_name '
                                   'FROM Procedure INNER JOIN Category '
                                   '     ON Procedure.category_id = Category.id '
                                   'ORDER BY Category.id').fetchall()

    return render_template('procedures.html', procedures=procedures,
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/procedures/<int:procedure_id>', methods=['GET'])
def edit_procedure_get(procedure_id):
    procedure = db.engine.execute('SELECT id, name, category_id, price_min, price_max, info '
                                  'FROM Procedure '
                                  'WHERE id = %s;',
                                  procedure_id).fetchone()

    categories = db.engine.execute('SELECT id, name '
                                   'FROM Category').fetchall()

    favourite_clients_amount = db.engine.execute('SELECT COUNT(*) '
                                                 'FROM Favourite_Procedure '
                                                 'WHERE procedure_id = %s;',
                                                 procedure_id).scalar()

    form = AdminProcedureForm(data=procedure)
    form.category_id.choices = [(category['id'], category['name']) for category in categories]

    return render_template('procedure.html', form=form,
                           favourite_clients_amount=favourite_clients_amount,
                           action=url_for('edit_procedure_post', procedure_id=procedure_id))


@app.route('/procedures/<int:procedure_id>', methods=['POST'])
def edit_procedure_post(procedure_id):
    form = AdminProcedureForm()

    categories = db.engine.execute('SELECT id, name '
                                   'FROM Category').fetchall()

    favourite_clients_amount = db.engine.execute('SELECT COUNT(*) '
                                                 'FROM Favourite_Procedure '
                                                 'WHERE procedure_id = %s;',
                                                 procedure_id).scalar()
    form.category_id.choices = [(category['id'], category['name']) for category in categories]

    if not form.validate_on_submit():
        return render_template('procedure.html', form=form,
                               favourite_clients_amount=favourite_clients_amount,
                               action=url_for('edit_procedure_post', procedure_id=procedure_id))

    procedure = Procedure(id=procedure_id)
    form.populate_obj(procedure)

    try:
        db.engine.execute('UPDATE Procedure '
                          'SET category_id = %s,'
                          '    name = %s,'
                          '    price_min = %s,'
                          '    price_max = %s, '
                          '    info = %s '
                          'WHERE id = %s;',
                          (procedure.category_id, procedure.name, procedure.price_min,
                           procedure.price_max, procedure.info, procedure.id))
    except IntegrityError:
        return render_template('procedure.html', form=form,
                               favourite_clients_amount=favourite_clients_amount,
                               action=url_for('edit_procedure_post', procedure_id=procedure_id),
                               error=get_error_message(Error.PROCEDURE_NAME_EXISTS.value))

    return redirect(url_for('procedures_get', success=Success.UPDATED_PROCEDURE.value))


@app.route('/procedures/new', methods=['GET'])
def new_procedure_get():
    categories = db.engine.execute('SELECT id, name '
                                   'FROM Category').fetchall()

    form = AdminProcedureForm()
    form.category_id.choices = [(category['id'], category['name']) for category in categories]

    return render_template('procedure.html', form=form,
                           action=url_for('new_procedure_post'))


@app.route('/procedures/new', methods=['POST'])
def new_procedure_post():
    form = AdminProcedureForm()
    categories = db.engine.execute('SELECT id, name '
                                   'FROM Category').fetchall()
    form.category_id.choices = [(category['id'], category['name']) for category in categories]

    if not form.validate_on_submit():
        return render_template('procedure.html', form=form,
                               action=url_for('new_procedure_post'))

    procedure = Procedure()
    form.populate_obj(procedure)

    try:
        db.engine.execute('INSERT INTO Procedure (category_id, name, price_min, price_max, info) '
                          'VALUES (%s, %s, %s, %s, %s);',
                          (procedure.category_id, procedure.name, procedure.price_min,
                           procedure.price_max, procedure.info))
    except IntegrityError:
        return render_template('procedure.html', form=form,
                               action=url_for('new_procedure_post'),
                               error=get_error_message(Error.PROCEDURE_NAME_EXISTS.value))

    return redirect(url_for('procedures_get', success=Success.ADDED_PROCEDURE.value))


@app.route('/procedures/delete/<int:procedure_id>', methods=['GET'])
def delete_procedure_get(procedure_id):
    try:
        db.engine.execute('DELETE '
                          'FROM Procedure '
                          'WHERE id = %s',
                          procedure_id)
    except IntegrityError:
        return redirect(url_for('procedures_get',
                                error=Error.PROCEDURE_HAS_APPOINTMENTS.value))

    return redirect(url_for('procedures_get', success=Success.DELETED_PROCEDURE.value))
