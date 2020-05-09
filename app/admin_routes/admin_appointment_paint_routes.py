from flask import render_template, request, redirect, url_for
from flask_login import login_required

from app import app
from app.models import *
from app.message_codes import *
from app.forms import AdminAppointmentPaintForm
from app.api.api_appointment_paint import *
from app.api.api_paint import get_spare_appointment_paints
from app.login import admin_only


@app.route('/appointments/<int:appointment_id>/paints/<int:paint_id>', methods=['GET'])
@login_required
@admin_only
def edit_appointment_paint_get(appointment_id, paint_id):
    appointment_paint = get_appointment_paint(appointment_id, paint_id)
    form = AdminAppointmentPaintForm(data=appointment_paint)
    form.paint_id.choices = [(str(appointment_paint.paint_id),
                              appointment_paint.paint_code + ' - ' + appointment_paint.paint_name)]
    form.paint_id.render_kw = {'readonly': ''}

    return render_template('appointment_paint.html', form=form, appointment_id=appointment_id,
                           action=url_for('edit_appointment_paint_post',
                                          appointment_id=appointment_id, paint_id=paint_id))


@app.route('/appointments/<int:appointment_id>/paints/<int:paint_id>', methods=['POST'])
@login_required
@admin_only
def edit_appointment_paint_post(appointment_id, paint_id):
    appointment_paint = get_appointment_paint(appointment_id, paint_id)
    form = AdminAppointmentPaintForm()
    form.paint_id.choices = [(str(appointment_paint.paint_id),
                              appointment_paint.paint_code + ' - ' + appointment_paint.paint_name)]
    form.paint_id.render_kw = {'readonly': ''}

    if not form.validate_on_submit():
        return render_template('appointment_paint.html', form=form, appointment_id=appointment_id,
                               action=url_for('edit_appointment_paint_post',
                                              appointment_id=appointment_id, paint_id=paint_id))

    appointment_paint = AppointmentPaint(appointment_id=appointment_id)
    form.populate_obj(appointment_paint)

    status, message = update_appointment_paint(appointment_paint)

    if status:
        return redirect(url_for('edit_appointment_get',
                                appointment_id=appointment_id, success=Success.UPDATED_APPOINTMENT_PAINT.value))
    else:
        return render_template('appointment_paint.html', form=form, appointment_id=appointment_id,
                               action=url_for('edit_appointment_paint_post',
                                              appointment_id=appointment_id, paint_id=paint_id),
                               error=message)


@app.route('/appointments/<int:appointment_id>/paints/new', methods=['GET'])
@login_required
@admin_only
def new_appointment_paint_get(appointment_id):
    form = AdminAppointmentPaintForm()
    form.paint_id.choices = [('', 'Не обрано')] + \
                            [(str(paint['id']), paint['code'] + ' - ' + paint['name'])
                             for paint in get_spare_appointment_paints(appointment_id)]

    return render_template('appointment_paint.html', form=form, appointment_id=appointment_id,
                           action=url_for('new_appointment_paint_post',
                                          appointment_id=appointment_id))


@app.route('/appointments/<int:appointment_id>/paints/new', methods=['POST'])
@login_required
@admin_only
def new_appointment_paint_post(appointment_id):
    form = AdminAppointmentPaintForm()
    form.paint_id.choices = [('', 'Не обрано')] + \
                            [(str(paint['id']), paint['code'] + ' - ' + paint['name'])
                             for paint in get_spare_appointment_paints(appointment_id)]

    if not form.validate_on_submit():
        return render_template('appointment_paint.html', form=form, appointment_id=appointment_id,
                               action=url_for('new_appointment_paint_post',
                                              appointment_id=appointment_id))

    appointment_paint = AppointmentPaint(appointment_id=appointment_id)
    form.populate_obj(appointment_paint)

    status, message = add_appointment_paint(appointment_paint)

    if status:
        return redirect(url_for('edit_appointment_get',
                                appointment_id=appointment_id, success=Success.ADDED_APPOINTMENT_PAINT.value))
    else:
        return render_template('appointment_paint.html', form=form, appointment_id=appointment_id,
                               action=url_for('new_appointment_paint_post',
                                              appointment_id=appointment_id),
                               error=message)


@app.route('/appointments/<int:appointment_id>/paints/delete/<int:paint_id>', methods=['GET'])
@login_required
@admin_only
def delete_appointment_paint_get(appointment_id, paint_id):
    status, message = delete_appointment_paint(appointment_id, paint_id)

    if status:
        return redirect(url_for('edit_appointment_get',
                                appointment_id=appointment_id, success=Success.DELETED_APPOINTMENT_PAINT.value))
    else:
        return redirect(url_for('edit_appointment_get',
                                appointment_id=appointment_id, error=Error.APPOINTMENT_PAINT_INTEGRITY.value))
