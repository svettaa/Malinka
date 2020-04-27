from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError, DataError

from app import app, db
from app.models import *


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

    return render_template('categories.html', categories=categories)


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

        new_name = request.form['categName']

        try:
            db.engine.execute('UPDATE Category '
                              'SET name = %s '
                              'WHERE id = %s;',
                              (new_name, category_id))
        except IntegrityError:
            return 'EXISTS'

        return redirect(url_for('categories'))


@app.route('/categories/new', methods=['POST', 'GET'])
def category_new():
    if request.method == 'GET':
        return render_template('category.html', category=None,
                               action=url_for('category_new'))

    if request.method == 'POST':
        new_name = request.form['categName']

        try:
            db.engine.execute('INSERT INTO Category (name) '
                              'VALUES (%s);',
                              new_name)
        except IntegrityError:
            return 'EXISTS'

        return redirect(url_for('categories'))


@app.route('/categories/delete/<int:category_id>')
def category_delete(category_id):
    try:
        db.engine.execute('DELETE '
                          'FROM Category '
                          'WHERE id = %s',
                          category_id)
    except IntegrityError:
        return "CATEGORY HAS PROCEDURES"

    return redirect(url_for('categories'))


@app.route('/procedures')
def procedures():
    procedures = db.engine.execute('SELECT Procedure.id, price_min, price_max, info, '
                                   '       Procedure.name AS procedure_name, '
                                   '       Category.name AS category_name '
                                   'FROM Procedure INNER JOIN Category '
                                   '     ON Procedure.category_id = Category.id '
                                   'ORDER BY Category.id').fetchall()

    return render_template('procedures.html', procedures=procedures)


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

        new_category_id = request.form['procCategID']
        new_name = request.form['procName']
        new_price_min = request.form['procMin']
        new_price_max = request.form['procMax']
        new_info = request.form['procInfo']

        if new_price_max.strip() == '':
            new_price_max = None

        try:
            db.engine.execute('UPDATE Procedure '
                              'SET category_id = %s,'
                              '    name = %s,'
                              '    price_min = %s,'
                              '    price_max = %s, '
                              '    info = %s '
                              'WHERE id = %s;',
                              (new_category_id, new_name, new_price_min,
                               new_price_max, new_info, procedure_id))
        except IntegrityError:
            return 'EXISTS'
        except DataError:
            return 'ILLEGAL DATA'

        return redirect(url_for('procedures'))


@app.route('/procedures/new', methods=['POST', 'GET'])
def procedure_new():
    if request.method == 'GET':

        categories = db.engine.execute('SELECT id, name '
                                       'FROM Category').fetchall()

        return render_template('procedure.html', procedure=None, categories=categories,
                               action=url_for('procedure_new'))

    if request.method == 'POST':
        new_category_id = request.form['procCategID']
        new_name = request.form['procName']
        new_price_min = request.form['procMin']
        new_price_max = request.form['procMax']
        new_info = request.form['procInfo']

        if new_price_max.strip() == '':
            new_price_max = None

        try:
            db.engine.execute('INSERT INTO Procedure (category_id, name, price_min, price_max, info) '
                              'VALUES (%s, %s, %s, %s, %s);',
                              (new_category_id, new_name, new_price_min,
                               new_price_max, new_info))
        except IntegrityError:
            return 'EXISTS'
        except DataError:
            return 'ILLEGAL DATA'

        return redirect(url_for('procedures'))


@app.route('/procedures/delete/<int:procedure_id>')
def procedure_delete(procedure_id):
    try:
        db.engine.execute('DELETE '
                          'FROM Procedure '
                          'WHERE id = %s',
                          procedure_id)
    except IntegrityError:
        return "PROCEDURE HAS APPOINTMENTS"

    return redirect(url_for('procedures'))
