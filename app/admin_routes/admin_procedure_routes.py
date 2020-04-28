from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError, DataError

from app import app
from app.models import *
from app.message_codes import *


@app.route('/procedures')
def procedures():
    procedures = db.engine.execute('SELECT Procedure.id, price_min, price_max, info, '
                                   '       Procedure.name AS procedure_name, '
                                   '       Category.name AS category_name '
                                   'FROM Procedure INNER JOIN Category '
                                   '     ON Procedure.category_id = Category.id '
                                   'ORDER BY Category.id').fetchall()

    return render_template('procedures.html', procedures=procedures,
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/procedures/<int:procedure_id>', methods=['POST', 'GET'])
def procedure(procedure_id):
    if request.method == 'GET':
        procedure = db.engine.execute('SELECT id, name, category_id, price_min, price_max, info '
                                      'FROM Procedure '
                                      'WHERE id = %s;',
                                      procedure_id).fetchone()

        categories = db.engine.execute('SELECT id, name '
                                       'FROM Category').fetchall()

        return render_template('procedure.html', procedure=procedure, categories=categories,
                               action=url_for('procedure', procedure_id=procedure_id))

    if request.method == 'POST':

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
                                   action=url_for('procedure', procedure_id=procedure_id),
                                   error=get_error_message(Error.PROCEDURE_NAME_EXISTS.value))
        except DataError:

            categories = db.engine.execute('SELECT id, name '
                                           'FROM Category').fetchall()
            return render_template('procedure.html', procedure=procedure, categories=categories,
                                   action=url_for('procedure', procedure_id=procedure_id),
                                   error=get_error_message(Error.PROCEDURE_ILLEGAL_DATA.value))

        return redirect(url_for('procedures', success=Success.UPDATED_PROCEDURE.value))


@app.route('/procedures/new', methods=['POST', 'GET'])
def procedure_new():
    if request.method == 'GET':
        categories = db.engine.execute('SELECT id, name '
                                       'FROM Category').fetchall()

        return render_template('procedure.html', procedure=None, categories=categories,
                               action=url_for('procedure_new'))

    if request.method == 'POST':

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
                                   action=url_for('procedure_new'),
                                   error=get_error_message(Error.PROCEDURE_NAME_EXISTS.value))
        except DataError:

            categories = db.engine.execute('SELECT id, name '
                                           'FROM Category').fetchall()
            return render_template('procedure.html', procedure=procedure, categories=categories,
                                   action=url_for('procedure_new'),
                                   error=get_error_message(Error.PROCEDURE_ILLEGAL_DATA.value))

        return redirect(url_for('procedures', success=Success.ADDED_PROCEDURE.value))


@app.route('/procedures/delete/<int:procedure_id>')
def procedure_delete(procedure_id):
    try:
        db.engine.execute('DELETE '
                          'FROM Procedure '
                          'WHERE id = %s',
                          procedure_id)
    except IntegrityError:
        return redirect(url_for('procedures',
                                error=Error.CATEGORY_HAS_PROCEDURES.value))

    return redirect(url_for('procedures', success=Success.DELETED_PROCEDURE.value))
