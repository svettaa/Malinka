from flask import render_template, request, redirect, url_for

from app import app
from app.message_codes import *
from app.forms import AdminCategoryForm
from app.api.api_category import *


@app.route('/categories')
def categories_get():
    return render_template('categories.html', categories=get_categories(),
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/categories/<int:category_id>', methods=['GET'])
def edit_category_get(category_id):
    form = AdminCategoryForm(data=get_category(category_id))

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

    status, message = update_category(category)

    if status:
        return redirect(url_for('categories_get', success=Success.UPDATED_CATEGORY.value))
    else:
        return render_template('category.html', form=form,
                               action=url_for('edit_category_post', category_id=category_id),
                               error=message)


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

    status, message = add_category(category)

    if status:
        return redirect(url_for('categories_get', success=Success.ADDED_CATEGORY.value))
    else:
        return render_template('category.html', form=form,
                               action=url_for('new_category_post'),
                               error=message)


@app.route('/categories/delete/<int:category_id>', methods=['GET'])
def delete_category_get(category_id):
    status, message = delete_category(category_id)

    if status:
        return redirect(url_for('categories_get', success=Success.DELETED_CATEGORY.value))
    else:
        return redirect(url_for('categories_get',
                                error=Error.CATEGORY_HAS_PROCEDURES.value))
