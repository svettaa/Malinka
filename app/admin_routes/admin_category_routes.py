from flask import render_template, request, redirect, url_for
from flask_login import login_required

from app import app
from app.forms import AdminCategoryForm
from app.api.api_category import *
from app.login import admin_only


@app.route('/categories')
@login_required
@admin_only
def categories_get():
    return render_template('categories.html', categories=get_categories(),
                           error=(request.args.get('error')),
                           success=(request.args.get('success')))


@app.route('/categories/<int:category_id>', methods=['GET'])
@login_required
@admin_only
def edit_category_get(category_id):
    form = AdminCategoryForm(data=get_category(category_id))

    return render_template('category.html', form=form,
                           action=url_for('edit_category_post', category_id=category_id))


@app.route('/categories/<int:category_id>', methods=['POST'])
@login_required
@admin_only
def edit_category_post(category_id):
    form = AdminCategoryForm()

    if not form.validate_on_submit():
        return render_template('category.html', form=form,
                               action=url_for('edit_category_post', category_id=category_id))

    category = Category(id=category_id)
    form.populate_obj(category)

    status, message = update_category(category)

    if status:
        return redirect(url_for('categories_get', success=message))
    else:
        return render_template('category.html', form=form,
                               action=url_for('edit_category_post', category_id=category_id),
                               error=message)


@app.route('/categories/new', methods=['GET'])
@login_required
@admin_only
def new_category_get():
    form = AdminCategoryForm()

    return render_template('category.html', form=form,
                           action=url_for('new_category_post'))


@app.route('/categories/new', methods=['POST'])
@login_required
@admin_only
def new_category_post():
    form = AdminCategoryForm()

    if not form.validate_on_submit():
        return render_template('category.html', form=form,
                               action=url_for('new_category_post'))

    category = Category()
    form.populate_obj(category)

    status, message = add_category(category)

    if status:
        return redirect(url_for('categories_get', success=message))
    else:
        return render_template('category.html', form=form,
                               action=url_for('new_category_post'),
                               error=message)


@app.route('/categories/delete/<int:category_id>', methods=['GET'])
@login_required
@admin_only
def delete_category_get(category_id):
    status, message = delete_category(category_id)

    if status:
        return redirect(url_for('categories_get', success=message))
    else:
        return redirect(url_for('categories_get',
                                error=message))
