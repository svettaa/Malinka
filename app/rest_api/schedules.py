import pytz
from flask import request
from flask_login import login_required

from app import app
from app.forms import AdminScheduleChangeForm
from app.db_api.schedules import *
from app.db_api.masters import *
from app.login import admin_only
from app.rest_api.utils import *


@app.route('/api/schedules', methods=['GET'])
@login_required
@admin_only
def api_schedules_get():
    return build_list_data_reply(get_schedules())


@app.route('/api/schedules/<int:schedule_id>', methods=['GET'])
@login_required
@admin_only
def api_schedule_get(schedule_id):
    return build_one_data_reply(get_schedule(schedule_id))


@app.route('/api/schedules', methods=['POST'])
@login_required
@admin_only
def api_schedule_post():
    form = AdminScheduleChangeForm(data=request.args)
    form.master_id.choices = [('', 'Не обрано')] + \
                             [(str(master['id']),
                               master['surname'] + ' ' + master['first_name'] + ', +38' + master['phone'])
                              for master in get_masters()]

    if not form.validate():
        return build_form_invalid_reply(form)

    schedule = ScheduleChange()
    form.populate_obj(schedule)
    schedule.change_start = pytz.timezone('Europe/Kiev').localize(schedule.change_start)
    schedule.change_end = pytz.timezone('Europe/Kiev').localize(schedule.change_end)

    return build_message_reply(add_schedule(schedule))


@app.route('/api/schedules/<int:schedule_id>', methods=['PUT'])
@login_required
@admin_only
def api_schedule_put(schedule_id):
    schedule = get_schedule(schedule_id)
    form = AdminScheduleChangeForm(data=request.args)
    form.master_id.choices = [(str(schedule.master_id),
                               schedule.master_surname + ' ' + schedule.master_first_name)]

    if not form.validate():
        return build_form_invalid_reply(form)

    schedule = ScheduleChange(id=schedule_id)
    form.populate_obj(schedule)
    schedule.change_start = pytz.timezone('Europe/Kiev').localize(schedule.change_start)
    schedule.change_end = pytz.timezone('Europe/Kiev').localize(schedule.change_end)

    return build_message_reply(update_schedule(schedule))


@app.route('/api/schedules/<int:schedule_id>', methods=['DELETE'])
@login_required
@admin_only
def api_schedule_delete(schedule_id):
    return build_message_reply(delete_schedule(schedule_id))
