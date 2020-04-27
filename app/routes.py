from flask import render_template, request, redirect, url_for

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


def exists_category_name(name, category_id=-1):
    scalar = db.engine.execute('SELECT * '
                               'FROM Category '
                               'WHERE name = %s AND id <> %s;',
                               name, category_id).scalar()
    return scalar is not None


def exists_category_procedures(category_id):
    scalar = db.engine.execute('SELECT * '
                               'FROM Procedure '
                               'WHERE category_id = %s;',
                               category_id).scalar()
    return scalar is not None


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

        if exists_category_name(new_name, category_id):
            return 'EXISTS'

        db.engine.execute('UPDATE Category '
                          'SET name = %s '
                          'WHERE id = %s;',
                          (new_name, category_id))

        return redirect(url_for('categories'))


@app.route('/categories/new', methods=['POST', 'GET'])
def category_new():
    if request.method == 'GET':
        return render_template('category.html', category=None,
                               action=url_for('category_new'))

    if request.method == 'POST':
        new_name = request.form['categName']

        if exists_category_name(new_name):
            return 'EXISTS'

        db.engine.execute('INSERT INTO Category (name) '
                          'VALUES (%s);',
                          new_name)

        return redirect(url_for('categories'))


@app.route('/categories/delete/<int:category_id>')
def category_delete(category_id):

    if exists_category_procedures(category_id):
        return "CATEGORY HAS PROCEDURES"

    db.engine.execute('DELETE '
                      'FROM Category '
                      'WHERE id = %s',
                      category_id)

    return redirect(url_for('categories'))


@app.route('/procedures')
def procedures():
    return render_template('procedures.html')


@app.route('/procedures/<int:procedure_id>')
def procedure(procedure_id):
    return render_template('procedure.html')
