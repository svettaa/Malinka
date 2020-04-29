from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError, DataError

from app import app
from app.models import *
from app.message_codes import *


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

    return render_template('procedure.html', procedure=procedure, categories=categories,
                           action=url_for('edit_procedure_post', procedure_id=procedure_id))


@app.route('/procedures/<int:procedure_id>', methods=['POST'])
def edit_procedure_post(procedure_id):
    procedure = Procedure(id=procedure_id, category_id=request.form['procCategID'],
                          name=request.form['procName'], price_min=request.form['procMin'],
                          price_max=request.form['procMax'], info=request.form['procInfo'])

    if procedure.price_max.strip() == '':
        procedure.price_max = None

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

        categories = db.engine.execute('SELECT id, name '
                                       'FROM Category').fetchall()
        return render_template('procedure.html', procedure=procedure, categories=categories,
                               action=url_for('edit_procedure_post', procedure_id=procedure_id),
                               error=get_error_message(Error.PROCEDURE_NAME_EXISTS.value))
    except DataError:

        categories = db.engine.execute('SELECT id, name '
                                       'FROM Category').fetchall()
        return render_template('procedure.html', procedure=procedure, categories=categories,
                               action=url_for('edit_procedure_post', procedure_id=procedure_id),
                               error=get_error_message(Error.PROCEDURE_ILLEGAL_DATA.value))

    return redirect(url_for('procedures_get', success=Success.UPDATED_PROCEDURE.value))


@app.route('/procedures/new', methods=['GET'])
def new_procedure_get():
    categories = db.engine.execute('SELECT id, name '
                                   'FROM Category').fetchall()

    return render_template('procedure.html', procedure=None, categories=categories,
                           action=url_for('new_procedure_post'))


@app.route('/procedures/new', methods=['POST'])
def new_procedure_post():
    procedure = Procedure(category_id=request.form['procCategID'],
                          name=request.form['procName'], price_min=request.form['procMin'],
                          price_max=request.form['procMax'], info=request.form['procInfo'])

    if procedure.price_max.strip() == '':
        procedure.price_max = None

    try:
        db.engine.execute('INSERT INTO Procedure (category_id, name, price_min, price_max, info) '
                          'VALUES (%s, %s, %s, %s, %s);',
                          (procedure.category_id, procedure.name, procedure.price_min,
                           procedure.price_max, procedure.info))
    except IntegrityError:

        categories = db.engine.execute('SELECT id, name '
                                       'FROM Category').fetchall()
        return render_template('procedure.html', procedure=procedure, categories=categories,
                               action=url_for('new_procedure_post'),
                               error=get_error_message(Error.PROCEDURE_NAME_EXISTS.value))
    except DataError:

        categories = db.engine.execute('SELECT id, name '
                                       'FROM Category').fetchall()
        return render_template('procedure.html', procedure=procedure, categories=categories,
                               action=url_for('new_procedure_post'),
                               error=get_error_message(Error.PROCEDURE_ILLEGAL_DATA.value))

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
