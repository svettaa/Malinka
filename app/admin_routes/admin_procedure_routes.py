from flask import render_template, request, redirect, url_for

from app import app
from app.message_codes import *
from app.forms import AdminProcedureForm
from app.api.api_procedure import *
from app.api.api_category import get_categories


@app.route('/procedures')
def procedures_get():
    return render_template('procedures.html', procedures=get_procedures(),
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/procedures/<int:procedure_id>', methods=['GET'])
def edit_procedure_get(procedure_id):
    form = AdminProcedureForm(data=get_procedure(procedure_id))
    form.category_id.choices = [('', 'Не обрано')] + \
                               [(str(category['id']), category['name']) for category in get_categories()]

    return render_template('procedure.html', form=form, new_procedure=False,
                           favourite_clients_amount=get_procedure_favourite_clients_amount(procedure_id),
                           action=url_for('edit_procedure_post', procedure_id=procedure_id))


@app.route('/procedures/<int:procedure_id>', methods=['POST'])
def edit_procedure_post(procedure_id):
    form = AdminProcedureForm()
    form.category_id.choices = [('', 'Не обрано')] + \
                               [(str(category['id']), category['name']) for category in get_categories()]

    if not form.validate_on_submit():
        return render_template('procedure.html', form=form, new_procedure=False,
                               favourite_clients_amount=get_procedure_favourite_clients_amount(procedure_id),
                               action=url_for('edit_procedure_post', procedure_id=procedure_id))

    procedure = Procedure(id=procedure_id)
    form.populate_obj(procedure)

    if procedure.info.strip() == '':
        procedure.info = None

    status, message = update_procedure(procedure)

    if status:
        return redirect(url_for('procedures_get', success=Success.UPDATED_PROCEDURE.value))
    else:
        return render_template('procedure.html', form=form, new_procedure=False,
                               favourite_clients_amount=get_procedure_favourite_clients_amount(procedure_id),
                               action=url_for('edit_procedure_post', procedure_id=procedure_id),
                               error=message)


@app.route('/procedures/new', methods=['GET'])
def new_procedure_get():
    form = AdminProcedureForm()
    form.category_id.choices = [('', 'Не обрано')] + \
                               [(str(category['id']), category['name']) for category in get_categories()]

    return render_template('procedure.html', form=form, new_procedure=True,
                           action=url_for('new_procedure_post'))


@app.route('/procedures/new', methods=['POST'])
def new_procedure_post():
    form = AdminProcedureForm()
    form.category_id.choices = [('', 'Не обрано')] + \
                               [(str(category['id']), category['name']) for category in get_categories()]

    if not form.validate_on_submit():
        return render_template('procedure.html', form=form, new_procedure=True,
                               action=url_for('new_procedure_post'))

    procedure = Procedure()
    form.populate_obj(procedure)

    if procedure.info.strip() == '':
        procedure.info = None

    status, message = add_procedure(procedure)

    if status:
        return redirect(url_for('procedures_get', success=Success.ADDED_PROCEDURE.value))
    else:
        return render_template('procedure.html', form=form, new_procedure=True,
                               action=url_for('new_procedure_post'),
                               error=message)


@app.route('/procedures/delete/<int:procedure_id>', methods=['GET'])
def delete_procedure_get(procedure_id):
    status, message = delete_procedure(procedure_id)

    if status:
        return redirect(url_for('procedures_get', success=Success.DELETED_PROCEDURE.value))
    else:
        return redirect(url_for('procedures_get',
                                error=Error.PROCEDURE_HAS_APPOINTMENTS.value))
