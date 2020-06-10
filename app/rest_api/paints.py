from flask import request
from flask_login import login_required

from app import app
from app.forms import AdminPaintForm
from app.db_api.paints import *
from app.login import admin_only
from app.rest_api.utils import *


@app.route('/api/paints', methods=['GET'])
@login_required
@admin_only
def api_paints_get():
    return build_list_data_reply(get_paints())


@app.route('/api/paints/<int:paint_id>', methods=['GET'])
@login_required
@admin_only
def api_paint_get(paint_id):
    return build_one_data_reply(get_paint(paint_id))


@app.route('/api/paints', methods=['POST'])
@login_required
@admin_only
def api_paint_post():
    form = AdminPaintForm(data=request.args)

    if not form.validate():
        return build_form_invalid_reply(form)

    paint = Paint()
    form.populate_obj(paint)

    return build_message_reply(add_paint(paint))


@app.route('/api/paints/<int:paint_id>', methods=['PUT'])
@login_required
@admin_only
def api_paint_put(paint_id):
    form = AdminPaintForm(data=request.args)

    if not form.validate():
        return build_form_invalid_reply(form)

    paint = Paint(id=paint_id)
    form.populate_obj(paint)

    return build_message_reply(update_paint(paint))


@app.route('/api/paints/<int:paint_id>', methods=['DELETE'])
@login_required
@admin_only
def api_paint_delete(paint_id):
    return build_message_reply(delete_paint(paint_id))
