from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError

from app import app
from app.models import *
from app.message_codes import *


@app.route('/categories')
def categories_get():
    categories = db.engine.execute('SELECT id, name '
                                   'FROM Category;').fetchall()

    return render_template('categories.html', categories=categories,
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/categories/<int:category_id>', methods=['GET'])
def edit_category_get(category_id):
    category = db.engine.execute('SELECT id, name '
                                 'FROM Category '
                                 'WHERE id = %s;',
                                 category_id).fetchone()

    return render_template('category.html', category=category,
                           action=url_for('edit_category_post', category_id=category_id))


@app.route('/categories/<int:category_id>', methods=['POST'])
def edit_category_post(category_id):
    category = Category(id=category_id, name=request.form['categName'])

    try:
        db.engine.execute('UPDATE Category '
                          'SET name = %s '
                          'WHERE id = %s;',
                          (category.name, category.id))
    except IntegrityError:
        return render_template('category.html', category=category,
                               action=url_for('edit_category_post', category_id=category_id),
                               error=get_error_message(Error.CATEGORY_NAME_EXISTS.value))

    return redirect(url_for('categories_get', success=Success.UPDATED_CATEGORY.value))


@app.route('/categories/new', methods=['GET'])
def new_category_get():
    return render_template('category.html', category=None,
                           action=url_for('new_category_post'))


@app.route('/categories/new', methods=['POST'])
def new_category_post():
    category = Category(name=request.form['categName'])

    try:
        db.engine.execute('INSERT INTO Category (name) '
                          'VALUES (%s);',
                          category.name)
    except IntegrityError:
        return render_template('category.html', category=category,
                               action=url_for('new_category_post'),
                               error=get_error_message(Error.CATEGORY_NAME_EXISTS.value))

    return redirect(url_for('categories_get', success=Success.ADDED_CATEGORY.value))


@app.route('/categories/delete/<int:category_id>', methods=['GET'])
def delete_category_get(category_id):
    try:
        db.engine.execute('DELETE '
                          'FROM Category '
                          'WHERE id = %s',
                          category_id)
    except IntegrityError:
        return redirect(url_for('categories_get',
                                error=Error.CATEGORY_HAS_PROCEDURES.value))

    return redirect(url_for('categories_get', success=Success.DELETED_CATEGORY.value))
