from flask import render_template, request, redirect, url_for
from flask_login import login_required

from app import app
from app.message_codes import *
from app.forms import AdminMasterForm
from app.api.api_master import *
from app.api.api_client import get_clients_no_masters
from app.login import admin_only


def get_master_and_their_procedures(master_id):
    master = get_master(master_id)
    procedures = get_all_procedures_join_master(master_id)
    return {'procedures': procedures,
            'id': master['id'],
            'surname': master['surname'],
            'first_name': master['first_name'],
            'second_name': master['second_name'],
            'phone': master['phone'],
            'even_schedule': master['even_schedule'],
            'is_male': master['is_male'],
            'email': master['email'],
            'is_hired': master['is_hired']}


@app.route('/masters', methods=['GET'])
@login_required
@admin_only
def masters_get():
    return render_template('masters.html', masters=get_masters(),
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/masters/<int:master_id>', methods=['GET'])
@login_required
@admin_only
def edit_master_get(master_id):
    data = get_master_and_their_procedures(master_id)
    form = AdminMasterForm(data=data)
    form.id.choices = [(str(data['id']),
                        data['surname'] + ' ' + data['first_name'] + ', +38' + data['phone'])]
    form.id.render_kw = {'readonly': ''}

    return render_template('master.html', master=get_master(master_id), form=form,
                           new_master=False,
                           favourite_clients_amount=get_master_favourite_clients_amount(master_id),
                           action=url_for('edit_master_post', master_id=master_id))


@app.route('/masters/<int:master_id>', methods=['POST'])
@login_required
@admin_only
def edit_master_post(master_id):
    master = get_master(master_id)
    form = AdminMasterForm()
    form.id.choices = [(str(master['id']),
                        master['surname'] + ' ' + master['first_name'] + ', +38' + master['phone'])]
    form.id.render_kw = {'readonly': ''}

    if not form.validate_on_submit():
        return render_template('master.html', master=get_master(master_id), form=form,
                               new_master=False,
                               favourite_clients_amount=get_master_favourite_clients_amount(master_id),
                               action=url_for('edit_master_post', master_id=master_id))

    master = Master(id=master_id, even_schedule=form.even_schedule.data, is_hired=form.is_hired.data)

    status, message = update_master(master)

    if status:
        pass
    else:
        return render_template('master.html', master=get_master(master_id), form=form,
                               new_master=False,
                               favourite_clients_amount=get_master_favourite_clients_amount(master_id),
                               action=url_for('edit_master_post', master_id=master_id),
                               error=message)

    status, message = update_master_procedures(master_id, form.procedures)

    if status:
        pass
    else:
        return render_template('master.html', master=get_master(master_id), form=form,
                               new_master=False,
                               favourite_clients_amount=get_master_favourite_clients_amount(master_id),
                               action=url_for('edit_master_post', master_id=master_id),
                               error=message)

    return redirect(url_for('masters_get', success=Success.UPDATED_MASTER.value))


@app.route('/masters/new', methods=['GET'])
@login_required
@admin_only
def new_master_get():
    form = AdminMasterForm()
    form.id.choices = [('', 'Не обрано')] + \
                      [(str(user['id']), user['surname'] + ' ' + user['first_name'] + ', +38' + user['phone'])
                       for user in get_clients_no_masters()]

    return render_template('master.html', form=form, new_master=True,
                           action=url_for('new_master_post'))


@app.route('/masters/new', methods=['POST'])
@login_required
@admin_only
def new_master_post():
    form = AdminMasterForm()
    form.id.choices = [('', 'Не обрано')] + \
                      [(str(user['id']), user['surname'] + ' ' + user['first_name'] + ', +38' + user['phone'])
                       for user in get_clients_no_masters()]

    if not form.validate_on_submit():
        return render_template('master.html', form=form, new_master=True,
                               action=url_for('new_master_post'))

    master = Master()
    form.populate_obj(master)

    status, message = add_master(master)

    if status:
        return redirect(url_for('masters_get', success=Success.ADDED_MASTER.value))
    else:
        return render_template('master.html', form=form, new_master=True,
                               action=url_for('new_master_post'),
                               error=message)


@app.route('/masters/delete/<int:master_id>', methods=['GET'])
@login_required
@admin_only
def delete_master_get(master_id):
    status, message = delete_master(master_id)

    if status:
        return redirect(url_for('masters_get', success=Success.DELETED_MASTER.value))
    else:
        return redirect(url_for('masters_get', error=Error.MASTER_HAS_APPOINTMENTS.value))
