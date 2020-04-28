from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError, DataError

from app import app, db
from app.models import *
from app.message_codes import *


@app.route('/')
def index():
    masters = db.engine.execute('SELECT surname, first_name, second_name '
                                'FROM Master;').fetchall()

    categories_proxy = db.engine.execute('SELECT id, name '
                                         'FROM Category;').fetchall()

    categories = []
    for category in categories_proxy:
        procedures = db.engine.execute('SELECT name, info, price_min, price_max '
                                       'FROM Procedure '
                                       'WHERE category_id = %s;',
                                       category['id']).fetchall()
        new_item = {'name': category['name'],
                    'procedures': procedures}
        categories.append(new_item)

    return render_template('index.html', categories=categories, masters=masters)


@app.route('/categories')
def categories():
    categories = db.engine.execute('SELECT id, name '
                                   'FROM Category;').fetchall()

    return render_template('categories.html', categories=categories,
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/categories/<int:category_id>', methods=['POST', 'GET'])
def category(category_id):
    if request.method == 'GET':
        category = db.engine.execute('SELECT id, name '
                                     'FROM Category '
                                     'WHERE id = %s;',
                                     category_id).fetchone()

        return render_template('category.html', category=category,
                               action=url_for('category', category_id=category_id))

    if request.method == 'POST':

        category = Category(id=category_id, name=request.form['categName'])

        try:
            db.engine.execute('UPDATE Category '
                              'SET name = %s '
                              'WHERE id = %s;',
                              (category.name, category.id))
        except IntegrityError:
            return render_template('category.html', category=category,
                                   action=url_for('category', category_id=category_id),
                                   error=get_error_message(Error.CATEGORY_NAME_EXISTS.value))

        return redirect(url_for('categories', success=Success.UPDATED_CATEGORY.value))


@app.route('/categories/new', methods=['POST', 'GET'])
def category_new():
    if request.method == 'GET':
        return render_template('category.html', category=None,
                               action=url_for('category_new'))

    if request.method == 'POST':
        category = Category(name=request.form['categName'])

        try:
            db.engine.execute('INSERT INTO Category (name) '
                              'VALUES (%s);',
                              category.name)
        except IntegrityError:
            return render_template('category.html', category=category,
                                   action=url_for('category_new'),
                                   error=get_error_message(Error.CATEGORY_NAME_EXISTS.value))

        return redirect(url_for('categories', success=Success.ADDED_CATEGORY.value))


@app.route('/categories/delete/<int:category_id>')
def category_delete(category_id):
    try:
        db.engine.execute('DELETE '
                          'FROM Category '
                          'WHERE id = %s',
                          category_id)
    except IntegrityError:
        return redirect(url_for('categories',
                                error=Error.CATEGORY_HAS_PROCEDURES.value))

    return redirect(url_for('categories', success=Success.DELETED_CATEGORY.value))


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


@app.route('/paints', methods=['GET'])
def paints_get():
    paints = db.engine.execute('SELECT id, code, name, left_ml '
                               'FROM Paint;').fetchall()

    return render_template('paints.html', paints=paints,
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/paints/<int:paint_id>', methods=['GET'])
def edit_paint_get(paint_id):
    paint = db.engine.execute('SELECT id, code, name, left_ml '
                              'FROM Paint '
                              'WHERE id = %s;',
                              paint_id).fetchone()

    return render_template('paint.html', paint=paint,
                           action=url_for('edit_paint_post', paint_id=paint_id))


@app.route('/paints/<int:paint_id>', methods=['POST'])
def edit_paint_post(paint_id):
    paint = Paint(id=paint_id, code=request.form['paintNum'],
                  name=request.form['paintName'], left_ml=request.form['paintLeft'])

    try:
        db.engine.execute('UPDATE Paint '
                          'SET code = %s,'
                          '    name = %s,'
                          '    left_ml = %s '
                          'WHERE id = %s;',
                          (paint.code, paint.name, paint.left_ml, paint.id))
    except IntegrityError:
        return render_template('paint.html', paint=paint,
                               action=url_for('edit_paint_post', paint_id=paint_id),
                               error=get_error_message(Error.PAINT_CODE_EXISTS.value))
    except DataError:
        return render_template('paint.html', paint=paint,
                               action=url_for('edit_paint_post', paint_id=paint.id),
                               error=get_error_message(Error.PAINT_ILLEGAL_DATA.value))

    return redirect(url_for('paints_get', success=Success.UPDATED_PAINT.value))


@app.route('/paints/new', methods=['GET'])
def new_paint_get():
    return render_template('paint.html', paint=None,
                           action=url_for('new_paint_post'))


@app.route('/paints/new', methods=['POST'])
def new_paint_post():
    paint = Paint(code=request.form['paintNum'],
                  name=request.form['paintName'], left_ml=request.form['paintLeft'])

    try:
        db.engine.execute('INSERT INTO Paint (code, name, left_ml) '
                          'VALUES (%s, %s, %s);',
                          (paint.code, paint.name, paint.left_ml))
    except IntegrityError:
        return render_template('paint.html', paint=paint,
                               action=url_for('new_paint_post', paint_id=paint.id),
                               error=get_error_message(Error.PAINT_CODE_EXISTS.value))
    except DataError:
        return render_template('paint.html', paint=paint,
                               action=url_for('new_paint_post', paint_id=paint.id),
                               error=get_error_message(Error.PAINT_ILLEGAL_DATA.value))

    return redirect(url_for('paints_get', success=Success.ADDED_PAINT.value))


@app.route('/paints/delete/<int:paint_id>', methods=['GET'])
def delete_paint_get(paint_id):
    try:
        db.engine.execute('DELETE '
                          'FROM Paint '
                          'WHERE id = %s',
                          paint_id)
    except IntegrityError:
        return redirect(url_for('paints_get',
                                error=Error.PAINT_HAS_APPOINTMENTS.value))

    return redirect(url_for('paints_get', success=Success.DELETED_PAINT.value))


@app.route('/supplies')
def supplies():
    return render_template('supplies.html')


@app.route('/supplies/<int:supply_id>')
def supply(supply_id):
    return render_template('supply.html')
