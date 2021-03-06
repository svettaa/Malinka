from flask import request
from flask_login import login_required

from app import app
from app.forms import AdminCategoryForm
from app.db_api.categories import *
from app.login import admin_only
from app.rest_api.utils import *


@app.route('/api/categories', methods=['GET'])
@login_required
@admin_only
def api_categories_get():
    return build_list_data_reply(get_categories())


@app.route('/api/categories/procedures', methods=['GET'])
@login_required
@admin_only
def api_categories_procedures_get():
    categories_proxy = db.engine.execute('SELECT id, name '
                                         'FROM Category;').fetchall()

    categories = []
    for category in categories_proxy:
        procedures = db.engine.execute('SELECT id, name, info, price_min, price_max, is_relevant '
                                       'FROM Procedure '
                                       'WHERE category_id = %s;',
                                       category['id']).fetchall()
        new_item = {'name': category['name'],
                    'procedures': json_list(procedures)}
        if len(procedures) > 0:
            categories.append(new_item)

    return jsonify({'status': True,
                    'data': categories})


@app.route('/api/categories/procedures/relevant', methods=['GET'])
def api_categories_procedures_relevant_get():
    categories_proxy = db.engine.execute('SELECT id, name '
                                         'FROM Category;').fetchall()

    categories = []
    for category in categories_proxy:
        procedures = db.engine.execute('SELECT id, name, info, price_min, price_max, is_relevant '
                                       'FROM Procedure '
                                       'WHERE category_id = %s AND is_relevant = True;',
                                       category['id']).fetchall()
        new_item = {'name': category['name'],
                    'procedures': json_list(procedures)}
        if len(procedures) > 0:
            categories.append(new_item)

    return jsonify({'status': True,
                    'data': categories})


@app.route('/api/categories/<int:category_id>', methods=['GET'])
@login_required
@admin_only
def api_category_get(category_id):
    return build_one_data_reply(get_category(category_id))


@app.route('/api/categories', methods=['POST'])
@login_required
@admin_only
def api_category_post():
    form = AdminCategoryForm(data=request.args)

    if not form.validate():
        return build_form_invalid_reply(form)

    category = Category()
    form.populate_obj(category)

    return build_message_reply(add_category(category))


@app.route('/api/categories/<int:category_id>', methods=['PUT'])
@login_required
@admin_only
def api_category_put(category_id):
    form = AdminCategoryForm(data=request.args)

    if not form.validate():
        return build_form_invalid_reply(form)

    category = Category(id=category_id)
    form.populate_obj(category)

    return build_message_reply(update_category(category))


@app.route('/api/categories/<int:category_id>', methods=['DELETE'])
@login_required
@admin_only
def api_category_delete(category_id):
    return build_message_reply(delete_category(category_id))
