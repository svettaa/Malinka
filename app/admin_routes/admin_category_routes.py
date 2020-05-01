from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError

from app import app
from app.models import *
from app.message_codes import *
from app.forms import AdminCategoryForm


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

    form = AdminCategoryForm(data=category)

    return render_template('category.html', form=form,
                           action=url_for('edit_category_post', category_id=category_id))


@app.route('/categories/<int:category_id>', methods=['POST'])
def edit_category_post(category_id):
    form = AdminCategoryForm()

    if not form.validate_on_submit():
        return render_template('category.html', form=form,
                               action=url_for('edit_category_post', category_id=category_id))

    category = Category(id=category_id)
    form.populate_obj(category)

    try:
        db.engine.execute('UPDATE Category '
                          'SET name = %s '
                          'WHERE id = %s;',
                          (category.name, category.id))
    except IntegrityError:
        return render_template('category.html', form=form,
                               action=url_for('edit_category_post', category_id=category_id),
                               error=get_error_message(Error.CATEGORY_NAME_EXISTS.value))

    return redirect(url_for('categories_get', success=Success.UPDATED_CATEGORY.value))


@app.route('/categories/new', methods=['GET'])
def new_category_get():
    form = AdminCategoryForm()

    return render_template('category.html', form=form,
                           action=url_for('new_category_post'))


@app.route('/categories/new', methods=['POST'])
def new_category_post():
    form = AdminCategoryForm()

    if not form.validate_on_submit():
        return render_template('category.html', form=form,
                               action=url_for('new_category_post'))

    category = Category()
    form.populate_obj(category)

    try:
        db.engine.execute('INSERT INTO Category (name) '
                          'VALUES (%s);',
                          category.name)
    except IntegrityError:
        return render_template('category.html', form=form,
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
