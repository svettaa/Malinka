from flask import render_template, request, redirect, url_for
from flask_login import login_required

from app import app
from app.api.api_appointment import *
from app.api.api_client import get_clients
from app.api.api_master import get_masters
from app.api.api_procedure import get_procedures
from app.api.api_appointment_paint import get_appointment_paints
from app.forms import AdminAppointmentForm
from app.login import admin_only


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
@login_required
@admin_only
def appointments_get():
    return render_template('appointments.html', appointments=get_appointments(),
                           error=(request.args.get('error')),
                           success=(request.args.get('success')))


@app.route('/appointments/<int:appointment_id>', methods=['GET'])
@login_required
@admin_only
def edit_appointment_get(appointment_id):
    appointment = get_appointment(appointment_id)
    form = AdminAppointmentForm(data=appointment)
    fill_edit_form_choices(form, appointment)

    return render_template('appointment.html', form=form, appointment_id=appointment_id,
                           paints=get_appointment_paints(appointment_id),
                           action=url_for('edit_appointment_post', appointment_id=appointment_id))


@app.route('/appointments/<int:appointment_id>', methods=['POST'])
@login_required
@admin_only
def edit_appointment_post(appointment_id):
    form = AdminAppointmentForm()
    fill_edit_form_choices(form, get_appointment(appointment_id))

    if not form.validate_on_submit():
        return render_template('appointment.html', form=form, appointment_id=appointment_id,
                               paints=get_appointment_paints(appointment_id),
                               action=url_for('edit_appointment_post', appointment_id=appointment_id))

    appointment = Appointment(id=appointment_id)
    form.populate_obj(appointment)

    if appointment.preferences.strip() == '':
        appointment.preferences = None

    status, message = update_appointment(appointment)

    if status:
        return redirect(url_for('appointments_get', success=message))
    else:
        return render_template('appointment.html', form=form,
                               paints=get_appointment_paints(appointment_id),
                               action=url_for('edit_appointment_post', appointment_id=appointment_id),
                               error=message)


@app.route('/appointments/new', methods=['GET'])
@login_required
@admin_only
def new_appointment_get():
    form = AdminAppointmentForm()
    fill_new_form_choices(form)

    return render_template('appointment.html', form=form,
                           action=url_for('new_appointment_post'))


@app.route('/appointments/new', methods=['POST'])
@login_required
@admin_only
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
        return redirect(url_for('appointments_get', success=message))
    else:
        return render_template('appointment.html', form=form,
                               action=url_for('new_appointment_post'),
                               error=message)


@app.route('/appointments/delete/<int:appointment_id>', methods=['GET'])
@login_required
@admin_only
def delete_appointment_get(appointment_id):
    status, message = delete_appointment(appointment_id)

    if status:
        return redirect(url_for('appointments_get', success=message))
    else:
        return redirect(url_for('appointments_get', error=message))
