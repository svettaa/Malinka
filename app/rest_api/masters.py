from flask import request
from flask_login import login_required

from app import app
from app.forms import AdminMasterForm2
from app.api.api_client import *
from app.api.api_master import *
from app.login import admin_only
from app.rest_api.utils import *


@app.route('/api/masters', methods=['GET'])
@login_required
@admin_only
def api_masters_get():
    return build_list_data_reply(get_masters())


@app.route('/api/masters/<int:master_id>', methods=['GET'])
@login_required
@admin_only
def api_master_get(master_id):
    return build_one_data_reply(get_master(master_id),
                                {'favourite_clients_amount': json_list(get_master_favourite_clients_amount(master_id))})


@app.route('/api/masters/<int:master_id>/procedures', methods=['GET'])
@login_required
@admin_only
def api_master_procedures_get(master_id):
    return build_list_data_reply(get_all_procedures_join_master(master_id))


@app.route('/api/masters/<int:master_id>/procedures', methods=['PUT'])
@login_required
@admin_only
def api_master_procedures_put(master_id):
    json = request.get_json()
    for json_part in json:
        if 'procedure_id' not in json_part or 'duration' not in json_part:
            return build_message_reply((False, 'Не вказано процедуру чи тривалість'))
        if type(json_part['procedure_id']) != int or type(json_part['duration']) != int:
            return build_message_reply((False, 'Мають бути цілі числа'))

    return build_message_reply(update_master_procedures(master_id, json))


@app.route('/api/masters', methods=['POST'])
@login_required
@admin_only
def api_master_post():
    form = AdminMasterForm2(data=request.args)
    form.id.choices = [('', 'Не обрано')] + \
                      [(str(user['id']), user['surname'] + ' ' + user['first_name'] + ', +38' + user['phone'])
                       for user in get_clients_no_masters()]

    if not form.validate():
        return build_form_invalid_reply(form)

    master = Master()
    form.populate_obj(master)

    return build_message_reply(add_master(master))


@app.route('/api/masters/<int:master_id>', methods=['PUT'])
@login_required
@admin_only
def api_master_put(master_id):
    form = AdminMasterForm2(data=request.args)
    form.id.choices = [(str(master_id), '')]

    if not form.validate():
        return build_form_invalid_reply(form)

    master = Master(id=master_id)
    form.populate_obj(master)

    return build_message_reply(update_master(master))


@app.route('/api/masters/<int:master_id>', methods=['DELETE'])
@login_required
@admin_only
def api_master_delete(master_id):
    return build_message_reply(delete_master(master_id))
