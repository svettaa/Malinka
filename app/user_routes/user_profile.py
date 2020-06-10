from flask import render_template, url_for, redirect, request
from flask_login import login_required, current_user

from app import app
from app.forms import AdminClientForm
from app.db_api.clients import *


@app.route('/cabinet/edit', methods=['GET'])
@login_required
def edit_user_profile_get():
    client_id = current_user.id
    form = AdminClientForm(data=get_client(client_id))
    return render_template('client.html', form=form, page_header='Мій кабінет',
                           user_view=True, csrf_token=AdminClientForm().csrf_token,
                           favourite_procedures=get_client_favourite_procedures(client_id),
                           favourite_masters=get_client_favourite_masters(client_id),
                           action=url_for('edit_user_profile_post'),
                           error=(request.args.get('error')),
                           success=(request.args.get('success')))


@app.route('/cabinet/edit', methods=['POST'])
@login_required
def edit_user_profile_post():
    form = AdminClientForm()
    client_id = current_user.id

    if not form.validate_on_submit():
        return render_template('client.html', form=form, page_header='Мій кабінет',
                               user_view=True,
                               favourite_procedures=get_client_favourite_procedures(client_id),
                               favourite_masters=get_client_favourite_masters(client_id),
                               action=url_for('edit_user_profile_post'))

    client = Client(id=client_id)
    form.populate_obj(client)

    if client.second_name.strip() == '':
        client.second_name = None
    if client.email.strip() == '':
        client.email = None

    status, message = update_client(client)

    if status:
        return redirect(url_for('edit_user_profile_get', success=message))
    else:
        return render_template('client.html', form=form, page_header='Мій кабінет',
                               user_view=True,
                               favourite_masters=get_client_favourite_masters(client_id),
                               favourite_procedures=get_client_favourite_procedures(client_id),
                               action=url_for('edit_user_profile_post'),
                               error=message)
