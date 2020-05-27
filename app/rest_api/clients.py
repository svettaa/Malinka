from flask import request
from flask_login import login_required

from app import app
from app.forms import AdminClientForm
from app.api.api_client import *
from app.login import admin_only
from app.rest_api.utils import *


@app.route('/api/clients', methods=['GET'])
@login_required
@admin_only
def api_clients_get():
    return build_list_data_reply(get_clients())


@app.route('/api/clients/not_masters', methods=['GET'])
@login_required
@admin_only
def api_clients_not_masters_get():
    return build_list_data_reply(get_clients_no_masters())


@app.route('/api/clients/<int:client_id>', methods=['GET'])
@login_required
@admin_only
def api_client_get(client_id):
    return build_one_data_reply(get_client(client_id),
                                {'favourite_masters': json_list(get_client_favourite_masters(client_id)),
                                 'favourite_procedures': json_list(get_client_favourite_procedures(client_id))})


@app.route('/api/clients', methods=['POST'])
@login_required
@admin_only
def api_client_post():
    form = AdminClientForm(data=request.args)

    if not form.validate():
        return build_form_invalid_reply(form)

    client = Client()
    form.populate_obj(client)

    if client.second_name.strip() == '':
        client.second_name = None
    if client.email.strip() == '':
        client.email = None

    return build_message_reply(add_client(client))


@app.route('/api/clients/<int:client_id>', methods=['PUT'])
@login_required
@admin_only
def api_client_put(client_id):
    form = AdminClientForm(data=request.args)

    if not form.validate():
        return build_form_invalid_reply(form)

    client = Client(id=client_id)
    form.populate_obj(client)

    if client.second_name.strip() == '':
        client.second_name = None
    if client.email.strip() == '':
        client.email = None

    return build_message_reply(update_client(client))


@app.route('/api/clients/<int:client_id>', methods=['DELETE'])
@login_required
@admin_only
def api_client_delete(client_id):
    return build_message_reply(delete_client(client_id))
