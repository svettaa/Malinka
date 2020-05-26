from flask import request
from flask_login import login_required

from app import app
from app.forms import AdminSupplyForm
from app.api.api_supply import *
from app.api.api_paint import *
from app.login import admin_only
from app.rest_api.utils import *


@app.route('/api/supplies', methods=['GET'])
@login_required
@admin_only
def api_supplies_get():
    return build_list_data_reply(get_supplies())


@app.route('/api/supplies/<int:supply_id>', methods=['GET'])
@login_required
@admin_only
def api_supply_get(supply_id):
    return build_one_data_reply(get_supply(supply_id))


@app.route('/api/supplies', methods=['POST'])
@login_required
@admin_only
def api_supply_post():
    form = AdminSupplyForm(data=request.args)
    form.paint_id.choices = [('', 'Не обрано')] + \
                            [(str(paint['id']), paint['code'] + ' - ' + paint['name']) for paint in get_paints()]

    if not form.validate():
        return build_form_invalid_reply(form)

    supply = PaintSupply()
    form.populate_obj(supply)

    return build_message_reply(add_supply(supply))


@app.route('/api/supplies/<int:supply_id>', methods=['PUT'])
@login_required
@admin_only
def api_supply_put(supply_id):
    form = AdminSupplyForm(data=request.args)
    form.paint_id.choices = [('', 'Не обрано')] + \
                            [(str(paint['id']), paint['code'] + ' - ' + paint['name']) for paint in get_paints()]

    if not form.validate():
        return build_form_invalid_reply(form)

    supply = PaintSupply(id=supply_id)
    form.populate_obj(supply)

    return build_message_reply(update_supply(supply))


@app.route('/api/supplies/<int:supply_id>', methods=['DELETE'])
@login_required
@admin_only
def api_supply_delete(supply_id):
    return build_message_reply(delete_supply(supply_id))
