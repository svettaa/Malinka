from flask import request
from flask_login import login_required

from app import app
from app.forms import AdminAppointmentPaintForm
from app.api.api_appointment_paint import *
from app.api.api_paint import *
from app.login import admin_only
from app.rest_api.utils import *


@app.route('/api/appointments/<int:appointment_id>/paints', methods=['GET'])
@login_required
@admin_only
def api_appointment_paints_get(appointment_id):
    return build_list_data_reply(get_appointment_paints(appointment_id))


@app.route('/api/appointments/<int:appointment_id>/paints/<int:paint_id>', methods=['GET'])
@login_required
@admin_only
def api_appointment_paint_get(appointment_id, paint_id):
    return build_one_data_reply(get_appointment_paint(appointment_id, paint_id))


@app.route('/api/appointments/<int:appointment_id>/paints', methods=['POST'])
@login_required
@admin_only
def api_appointment_paint_post(appointment_id):
    form = AdminAppointmentPaintForm(data=request.args)
    form.paint_id.choices = [('', 'Не обрано')] + \
                            [(str(paint['id']), paint['code'] + ' - ' + paint['name'])
                             for paint in get_spare_appointment_paints(appointment_id)]

    if not form.validate():
        return build_form_invalid_reply(form)

    appointment_paint = AppointmentPaint(appointment_id=appointment_id)
    form.populate_obj(appointment_paint)

    return build_message_reply(add_appointment_paint(appointment_paint))


@app.route('/api/appointments/<int:appointment_id>/paints/<int:paint_id>', methods=['PUT'])
@login_required
@admin_only
def api_appointment_paint_put(appointment_id, paint_id):
    appointment_paint = get_appointment_paint(appointment_id, paint_id)
    form = AdminAppointmentPaintForm(data=request.args)
    form.paint_id.choices = [(str(appointment_paint.paint_id),
                              appointment_paint.paint_code + ' - ' + appointment_paint.paint_name)]

    if not form.validate():
        return build_form_invalid_reply(form)

    appointment_paint = AppointmentPaint(appointment_id=appointment_id)
    form.populate_obj(appointment_paint)

    return build_message_reply(update_appointment_paint(appointment_paint))


@app.route('/api/appointments/<int:appointment_id>/paints/<int:paint_id>', methods=['DELETE'])
@login_required
@admin_only
def api_appointment_paint_delete(appointment_id, paint_id):
    return build_message_reply(delete_appointment_paint(appointment_id, paint_id))
