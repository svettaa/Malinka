from flask import request
from flask_login import login_required

from app import app
from app.forms import AdminProcedureForm
from app.api.api_procedure import *
from app.api.api_category import *
from app.login import admin_only
from app.rest_api.utils import *


@app.route('/api/procedures', methods=['GET'])
@login_required
@admin_only
def api_procedures_get():
    return build_list_data_reply(get_procedures())


@app.route('/api/procedures/<int:procedure_id>', methods=['GET'])
@login_required
@admin_only
def api_procedure_get(procedure_id):
    return build_one_data_reply(get_procedure(procedure_id),
                                {'favourite_clients': get_procedure_favourite_clients_amount(procedure_id)})


@app.route('/api/procedures', methods=['POST'])
@login_required
@admin_only
def api_procedure_post():
    form = AdminProcedureForm(data=request.args)
    form.category_id.choices = [('', 'Не обрано')] + \
                               [(str(category['id']), category['name']) for category in get_categories()]

    if not form.validate():
        return build_form_invalid_reply(form)

    procedure = Procedure()
    form.populate_obj(procedure)

    if procedure.info.strip() == '':
        procedure.info = None

    return build_message_reply(add_procedure(procedure))


@app.route('/api/procedures/<int:procedure_id>', methods=['PUT'])
@login_required
@admin_only
def api_procedure_put(procedure_id):
    form = AdminProcedureForm(data=request.args)

    if not form.validate():
        return build_form_invalid_reply(form)

    procedure = Procedure(id=procedure_id)
    form.populate_obj(procedure)

    if procedure.info.strip() == '':
        procedure.info = None

    return build_message_reply(update_procedure(procedure))


@app.route('/api/procedures/<int:procedure_id>', methods=['DELETE'])
@login_required
@admin_only
def api_procedure_delete(procedure_id):
    return build_message_reply(delete_procedure(procedure_id))
