from flask_socketio import emit
from flask_login import login_required
from datetime import datetime

from app import socketio, app
from app.login import admin_only
from app.socket_io import json_one, json_list
from app.api.api_appointment import get_master_date_appointments
from app.api.api_master import *


def normalize_time(start, end, date_obj):
    if start.date() < date_obj.date():
        start_time = app.config['WORKING_DAY_START']
    else:
        start_time = max(start.time(), app.config['WORKING_DAY_START'])

    if end.date() > date_obj.date():
        end_time = app.config['WORKING_DAY_END']
    else:
        end_time = min(end.time(), app.config['WORKING_DAY_END'])

    return {'start': start_time.strftime('%H:%M'),
            'end': end_time.strftime('%H:%M')}


def get_vacations_list(master_id, date_obj):
    result = list()
    for vacation in get_master_date_vacations(master_id, date_obj):
        result.append \
            (json_one(normalize_time(vacation.change_start, vacation.change_end, date_obj)))
    return result


def get_appointments_list(master_id, date_obj):
    result = list()
    for appointment in get_master_date_appointments(master_id, date_obj):
        result.append \
            (json_one(normalize_time(appointment.appoint_start, appointment.appoint_end, date_obj)))
    return result


def get_not_working_list(master_id, date_obj):
    even_day = (date_obj.day % 2 == 0)
    if get_master(master_id).even_schedule == even_day:
        return []

    overworks = list()
    for overwork in get_master_date_overworks(master_id, date_obj):
        overworks.append \
            (json_one(normalize_time(overwork.change_start, overwork.change_end, date_obj)))

    result = []
    next_start = app.config['WORKING_DAY_START'].strftime('%H:%M')

    for overwork in overworks:
        result.append({'start': next_start, 'end': overwork['start']})
        next_start = overwork['end']

    result.append({'start': next_start, 'end': app.config['WORKING_DAY_END'].strftime('%H:%M')})
    return result


@socketio.on('get_journal', namespace='/admin')
@login_required
@admin_only
def get_journal(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d.%m.%Y')

        masters = json_list(get_masters_working(date_obj))

        for master in masters:
            master['appointments'] = json_list(get_master_date_appointments(master['id'], date_obj))
            master['vacations'] = get_vacations_list(master['id'], date_obj)
            master['notWorking'] = get_not_working_list(master['id'], date_obj)

        emit('get_journal', {'status': True,
                             'data': masters}, json=True)
    except ValueError:
        emit('get_journal', {'status': False,
                             'message': 'Некоректний формат часу'}, json=True)
