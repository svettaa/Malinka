from flask import render_template, request, redirect, url_for

from app import app
from app.api.api_appointment import *
from app.api.api_client import get_clients
from app.api.api_master import get_masters
from app.api.api_procedure import get_procedures
from app.forms import AdminAppointmentForm
from app.message_codes import *


def fill_new_form_choices(form):
    form.master_id.choices = [('', 'Не обрано')] + \
                             [(str(master['id']), master['surname'] + ' ' + master['first_name'])
                              for master in get_masters()]
    form.client_id.choices = [('', 'Не обрано')] + \
                             [(str(user['id']), user['surname'] + ' ' + user['first_name'] + ', +38' + user['phone'])
                              for user in get_clients()]
    form.procedure_id.choices = [('', 'Не обрано')] + \
                                [(str(procedure['id']), procedure['procedure_name'])
                                 for procedure in get_procedures()]


def fill_edit_form_choices(form, appointment):
    form.master_id.choices = [(str(appointment.master_id),
                               appointment.master_surname + ' ' + appointment.master_first_name)]
    form.client_id.choices = [(str(appointment.client_id),
                               appointment.client_surname + ' ' + appointment.client_first_name +
                               ', +38' + appointment.client_phone)]
    form.procedure_id.choices = [('', 'Не обрано')] + \
                                [(str(procedure['id']), procedure['procedure_name'])
                                 for procedure in get_procedures()]
    form.master_id.render_kw = form.client_id.render_kw = {'readonly': ''}


@app.route('/appointments')
def appointments_get():
    return render_template('appointments.html', appointments=get_appointments(),
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/appointments/<int:appointment_id>', methods=['GET'])
def edit_appointment_get(appointment_id):
    appointment = get_appointment(appointment_id)
    form = AdminAppointmentForm(data=appointment)
    fill_edit_form_choices(form, appointment)

    return render_template('appointment.html', form=form,
                           action=url_for('edit_appointment_post', appointment_id=appointment_id))


@app.route('/appointments/<int:appointment_id>', methods=['POST'])
def edit_appointment_post(appointment_id):
    form = AdminAppointmentForm()
    fill_edit_form_choices(form, get_appointment(appointment_id))

    if not form.validate_on_submit():
        return render_template('appointment.html', form=form,
                               action=url_for('edit_appointment_post', appointment_id=appointment_id))

    appointment = Appointment(id=appointment_id)
    form.populate_obj(appointment)

    if appointment.preferences.strip() == '':
        appointment.preferences = None

    status, message = update_appointment(appointment)

    if status:
        return redirect(url_for('appointments_get', success=Success.UPDATED_APPOINTMENT.value))
    else:
        return render_template('appointment.html', form=form,
                               action=url_for('edit_appointment_post', appointment_id=appointment_id),
                               error=message)


@app.route('/appointments/new', methods=['GET'])
def new_appointment_get():
    form = AdminAppointmentForm()
    fill_new_form_choices(form)

    return render_template('appointment.html', form=form,
                           action=url_for('new_appointment_post'))


@app.route('/appointments/new', methods=['POST'])
def new_appointment_post():
    form = AdminAppointmentForm()
    fill_new_form_choices(form)

    if not form.validate_on_submit():
        return render_template('appointment.html', form=form,
                               action=url_for('new_appointment_post'))

    appointment = Appointment()
    form.populate_obj(appointment)

    if appointment.preferences.strip() == '':
        appointment.preferences = None

    status, message = add_appointment(appointment)

    if status:
        return redirect(url_for('appointments_get', success=Success.ADDED_APPOINTMENT.value))
    else:
        return render_template('appointment.html', form=form,
                               action=url_for('new_appointment_post'),
                               error=message)


@app.route('/appointments/delete/<int:appointment_id>', methods=['GET'])
def delete_appointment_get(appointment_id):
    status, message = delete_appointment(appointment_id)

    if status:
        return redirect(url_for('appointments_get', success=Success.DELETED_APPOINTMENT.value))
    else:
        return redirect(url_for('appointments_get', error=Error.APPOINTMENT_INTEGRITY.value))
