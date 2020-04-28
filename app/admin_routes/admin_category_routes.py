from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError

from app import app
from app.models import *
from app.message_codes import *


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
