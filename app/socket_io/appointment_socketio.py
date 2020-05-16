from flask_socketio import emit

from app import socketio, app
from app.socket_io import json_one, json_list
from app.api.api_master import *
from app.socket_io.journal_socketio import get_vacations_list, get_not_working_list, get_appointments_list


def fill_free_time(master, date_obj):
    appointments = get_appointments_list(master['id'], date_obj)
    vacations = get_vacations_list(master['id'], date_obj)
    not_works = get_not_working_list(master['id'], date_obj)

    occupied_time = appointments + vacations + not_works
    occupied_time.sort(key=lambda x: x['start'])

    result = []
    next_start = app.config['WORKING_DAY_START'].strftime('%H:%M')
    for occ in occupied_time:
        result.append({'start': next_start, 'end': occ['start']})
        next_start = occ['end']
    result.append({'start': next_start, 'end': app.config['WORKING_DAY_END'].strftime('%H:%M')})

    master['freeTime'] = result


@socketio.on('get_free_time', namespace='/appointment')
def get_free_time(data):
    print('hot shtoto')
    try:
        date_obj = datetime.strptime(data['date'], '%d.%m.%Y')
        procedure_id = data['procedure']

        masters = json_list(get_masters_working_do_procedure_client_view(date_obj, procedure_id))

        for master in masters:
            fill_free_time(master, date_obj)

        emit('get_free_time', {'status': True,
                               'data': masters}, json=True)
    except ValueError:
        emit('get_free_time', {'status': False,
                               'message': 'Некоректний формат часу'}, json=True)
