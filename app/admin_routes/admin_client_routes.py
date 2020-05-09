from flask import render_template, request, redirect, url_for
from flask_login import login_required

from app import app
from app.models import *
from app.message_codes import *
from app.forms import AdminClientForm
from app.api.api_client import *
from app.login import admin_only


@app.route('/clients', methods=['GET'])
@login_required
@admin_only
def clients_get():
    return render_template('clients.html', clients=get_clients(),
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/clients/<int:client_id>', methods=['GET'])
@login_required
@admin_only
def edit_client_get(client_id):
    form = AdminClientForm(data=get_client(client_id))

    return render_template('client.html', form=form,
                           favourite_procedures=get_client_favourite_procedures(client_id),
                           favourite_masters=get_client_favourite_masters(client_id),
                           action=url_for('edit_client_post', client_id=client_id))


@app.route('/clients/<int:client_id>', methods=['POST'])
@login_required
@admin_only
def edit_client_post(client_id):
    form = AdminClientForm()

    if not form.validate_on_submit():
        return render_template('client.html', form=form,
                               favourite_procedures=get_client_favourite_procedures(client_id),
                               favourite_masters=get_client_favourite_masters(client_id),
                               action=url_for('edit_client_post', client_id=client_id))

    client = Client(id=client_id)
    form.populate_obj(client)

    if client.second_name.strip() == '':
        client.second_name = None
    if client.email.strip() == '':
        client.email = None

    status, message = update_client(client)

    if status:
        return redirect(url_for('clients_get', success=Success.UPDATED_USER.value))
    else:
        return render_template('client.html', form=form,
                               favourite_masters=get_client_favourite_masters(client_id),
                               favourite_procedures=get_client_favourite_procedures(client_id),
                               action=url_for('edit_client_post', client_id=client_id),
                               error=message)


@app.route('/clients/new', methods=['GET'])
@login_required
@admin_only
def new_client_get():
    form = AdminClientForm()

    return render_template('client.html', form=form,
                           action=url_for('new_client_post'))


@app.route('/clients/new', methods=['POST'])
@login_required
@admin_only
def new_client_post():
    form = AdminClientForm()

    if not form.validate_on_submit():
        return render_template('client.html', form=form,
                               action=url_for('new_client_post'))

    client = Client()
    form.populate_obj(client)

    if client.second_name.strip() == '':
        client.second_name = None
    if client.email.strip() == '':
        client.email = None

    status, message = add_client(client)

    if status:
        return redirect(url_for('clients_get', success=Success.ADDED_USER.value))
    else:
        return render_template('client.html', form=form,
                               action=url_for('new_client_post'),
                               error=message)


@app.route('/clients/delete/<int:client_id>', methods=['GET'])
@login_required
@admin_only
def delete_client_get(client_id):

    status, message = delete_client(client_id)

    if status:
        return redirect(url_for('clients_get', success=Success.DELETED_USER.value))
    else:
        return redirect(url_for('clients_get',
                                error=Error.USER_HAS_APPOINTMENTS.value))
