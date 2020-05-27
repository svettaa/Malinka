from flask import request
from flask_login import login_required

from app import app
from app.forms import AdminAppointmentForm
from app.api.api_appointment import *
from app.api.api_master import *
from app.api.api_client import *
from app.api.api_procedure import *
from app.api.api_appointment_paint import *
from app.login import admin_only
from app.rest_api.utils import *


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


@app.route('/api/appointments', methods=['GET'])
@login_required
@admin_only
def api_appointments_get():
    return build_list_data_reply(get_appointments())


@app.route('/api/appointments/<int:appointment_id>', methods=['GET'])
@login_required
@admin_only
def api_appointment_get(appointment_id):
    return build_one_data_reply(get_appointment(appointment_id))


@app.route('/api/appointments/<int:appointment_id>/paints', methods=['GET'])
@login_required
@admin_only
def api_appointment_paints_get(appointment_id):
    return build_list_data_reply(get_appointment_paints(appointment_id))


@app.route('/api/appointments', methods=['POST'])
@login_required
@admin_only
def api_appointment_post():
    form = AdminAppointmentForm(data=request.args)
    fill_new_form_choices(form)

    if not form.validate():
        return build_form_invalid_reply(form)

    appointment = Appointment()
    form.populate_obj(appointment)
    appointment.appoint_start = pytz.timezone('Europe/Kiev').localize(appointment.appoint_start)
    appointment.appoint_end = pytz.timezone('Europe/Kiev').localize(appointment.appoint_end)

    if appointment.preferences.strip() == '':
        appointment.preferences = None

    return build_message_reply(add_appointment(appointment))


@app.route('/api/appointments/<int:appointment_id>', methods=['PUT'])
@login_required
@admin_only
def api_appointment_put(appointment_id):
    form = AdminAppointmentForm(data=request.args)
    fill_edit_form_choices(form, get_appointment(appointment_id))

    if not form.validate():
        return build_form_invalid_reply(form)

    appointment = Appointment(id=appointment_id)
    form.populate_obj(appointment)
    appointment.appoint_start = pytz.timezone('Europe/Kiev').localize(appointment.appoint_start)
    appointment.appoint_end = pytz.timezone('Europe/Kiev').localize(appointment.appoint_end)

    if appointment.preferences.strip() == '':
        appointment.preferences = None

    return build_message_reply(update_appointment(appointment))


@app.route('/api/appointments/<int:appointment_id>', methods=['DELETE'])
@login_required
@admin_only
def api_appointment_delete(appointment_id):
    return build_message_reply(delete_appointment(appointment_id))
