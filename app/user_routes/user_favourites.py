from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app import app
from app.api.api_client import *
from app.api.api_master import get_masters
from app.api.api_procedure import get_procedures
from app.forms import AddFavouriteMaster, AddFavouriteProcedure


@app.route('/cabinet/favourite_procedures/new', methods=['GET'])
@login_required
def new_favourite_procedure_get():
    form = AddFavouriteProcedure()
    form.procedure_id.choices = [('', 'Не обрано')] + \
                                [(str(procedure['id']), procedure['procedure_name'])
                                 for procedure in get_procedures()]

    return render_template('add_favourite_procedure.html', form=form)


@app.route('/cabinet/favourite_procedures/new', methods=['POST'])
@login_required
def new_favourite_procedure_post():
    form = AddFavouriteProcedure()
    form.procedure_id.choices = [('', 'Не обрано')] + \
                                [(str(procedure['id']), procedure['procedure_name'])
                                 for procedure in get_procedures()]

    if not form.validate_on_submit():
        return render_template('add_favourite_procedure.html', form=form)

    status, message = add_client_favourite_procedure(current_user.id, form.procedure_id.data)

    if status:
        return redirect(url_for('edit_user_profile_get', success=message))
    else:
        return render_template('add_favourite_procedure.html', form=form,
                               error=message)


@app.route('/cabinet/favourite_masters/new', methods=['GET'])
@login_required
def new_favourite_master_get():
    form = AddFavouriteMaster()
    form.master_id.choices = [('', 'Не обрано')] + \
                             [(str(master['id']),
                               master['surname'] + ' ' + master['first_name'])
                              for master in get_masters()]

    return render_template('add_favourite_master.html', form=form)


@app.route('/cabinet/favourite_masters/new', methods=['POST'])
@login_required
def new_favourite_master_post():
    form = AddFavouriteMaster()
    form.master_id.choices = [('', 'Не обрано')] + \
                             [(str(master['id']),
                               master['surname'] + ' ' + master['first_name'])
                              for master in get_masters()]

    if not form.validate_on_submit():
        return render_template('add_favourite_master.html', form=form)

    status, message = add_client_favourite_master(current_user.id, form.master_id.data)

    if status:
        return redirect(url_for('edit_user_profile_get', success=message))
    else:
        return render_template('add_favourite_master.html', form=form,
                               error=message)


@app.route('/cabinet/favourite_masters/delete/<int:master_id>', methods=['GET'])
@login_required
def delete_favourite_master_get(master_id):
    status, message = delete_client_favourite_master(current_user.id, master_id)

    if status:
        return redirect(url_for('edit_user_profile_get',
                                success=message))
    else:
        return redirect(url_for('edit_user_profile_get',
                                error=message))


@app.route('/cabinet/favourite_procedures/delete/<int:procedure_id>', methods=['GET'])
@login_required
def delete_favourite_procedure_get(procedure_id):
    status, message = delete_client_favourite_procedure(current_user.id, procedure_id)

    if status:
        return redirect(url_for('edit_user_profile_get',
                                success=message))
    else:
        return redirect(url_for('edit_user_profile_get',
                                error=message))
