from flask import request
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash

from app import app, get_masters, get_procedures, get_client_future_appointments, get_client_past_appointments, \
    delete_appointment_if_future
from app.forms import AdminClientForm, ChangePasswordForm, AddFavouriteMaster, AddFavouriteProcedure
from app.db_api.clients import *
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
def api_client_get(client_id):
    if not current_user.is_admin() and current_user.id != client_id:
        return build_message_reply((False, 'Заборонено доступ'))
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
def api_client_put(client_id):
    if not current_user.is_admin() and current_user.id != client_id:
        return build_message_reply((False, 'Заборонено доступ'))
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


@app.route('/api/clients/<int:client_id>/favourite_masters', methods=['POST'])
@login_required
def api_client_favourite_master_put(client_id):
    if current_user.id != client_id:
        return build_message_reply((False, 'Заборонено доступ'))

    form = AddFavouriteMaster()
    form.master_id.choices = [('', 'Не обрано')] + \
                             [(str(master['id']),
                               master['surname'] + ' ' + master['first_name'])
                              for master in get_masters()]

    if not form.validate_on_submit():
        return build_form_invalid_reply(form)

    return build_message_reply(add_client_favourite_master(current_user.id, form.master_id.data))


@app.route('/api/clients/<int:client_id>/favourite_masters/<int:master_id>', methods=['DELETE'])
@login_required
def api_client_favourite_master_delete(client_id, master_id):
    if current_user.id != client_id:
        return build_message_reply((False, 'Заборонено доступ'))

    return build_message_reply(delete_client_favourite_master(current_user.id, master_id))


@app.route('/api/clients/<int:client_id>/favourite_procedures', methods=['POST'])
@login_required
def api_client_favourite_procedure_put(client_id):
    if current_user.id != client_id:
        return build_message_reply((False, 'Заборонено доступ'))

    form = AddFavouriteProcedure()
    form.procedure_id.choices = [('', 'Не обрано')] + \
                                [(str(procedure['id']), procedure['procedure_name'])
                                 for procedure in get_procedures()]

    if not form.validate_on_submit():
        return build_form_invalid_reply(form)

    return build_message_reply(add_client_favourite_procedure(current_user.id, form.procedure_id.data))


@app.route('/api/clients/<int:client_id>/favourite_procedures/<int:procedure_id>', methods=['DELETE'])
@login_required
def api_client_favourite_procedure_delete(client_id, procedure_id):
    if current_user.id != client_id:
        return build_message_reply((False, 'Заборонено доступ'))

    return build_message_reply(delete_client_favourite_procedure(current_user.id, procedure_id))


@app.route('/api/clients/<int:client_id>/password', methods=['PUT'])
@login_required
def api_user_password_put(client_id):
    if current_user.id != client_id:
        return build_message_reply((False, 'Заборонено доступ'))

    form = ChangePasswordForm()

    if not check_password_hash(get_client_password(client_id), form.old_password.data):
        return build_message_reply((False, 'Неправильний старий пароль'))

    if not form.validate_on_submit():
        return build_form_invalid_reply(form)

    return build_message_reply(set_client_password(client_id, form.new_password.data))


@app.route('/api/clients/<int:client_id>/appointments', methods=['GET'])
@login_required
def api_user_appointments_get(client_id):
    if current_user.id != client_id:
        return build_message_reply((False, 'Заборонено доступ'))

    return build_one_data_reply({'future': json_list(get_client_future_appointments(client_id)),
                                 'past': json_list(get_client_past_appointments(client_id))})


@app.route('/api/clients/<int:client_id>/appointments/<int:appointment_id>', methods=['DELETE'])
@login_required
def api_user_appointments_delete(client_id, appointment_id):
    if current_user.id != client_id:
        return build_message_reply((False, 'Заборонено доступ'))

    return build_message_reply(delete_appointment_if_future(appointment_id, client_id))


@app.route('/api/clients/<int:client_id>', methods=['DELETE'])
@login_required
@admin_only
def api_client_delete(client_id):
    return build_message_reply(delete_client(client_id))
