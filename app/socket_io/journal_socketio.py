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
        start_time = start.time()

    if end.date() > date_obj.date():
        end_time = app.config['WORKING_DAY_END']
    else:
        end_time = end.time()

    return {'start': start_time.strftime('%H:%M'),
            'end': end_time.strftime('%H:%M')}


@socketio.on('get_journal', namespace='/admin')
@login_required
@admin_only
def get_journal(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d.%m.%Y')

        masters = json_list(get_masters_working(date_obj))

        for master in masters:
            master['appointments'] = json_list(get_master_date_appointments(master['id'], date_obj))
            master['vacations'] = list()
            for vacation in get_master_date_vacations(master['id'], date_obj):
                master['vacations'].append\
                    (json_one(normalize_time(vacation.change_start, vacation.change_end, date_obj)))

        emit('get_journal', {'status': True,
                             'data': masters}, json=True)
    except ValueError:
        emit('get_journal', {'status': False,
                             'message': 'Некоректний формат часу'}, json=True)
