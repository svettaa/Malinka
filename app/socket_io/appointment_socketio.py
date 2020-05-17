from flask_socketio import emit
from flask_login import current_user

from app import socketio, app
from app.socket_io import json_one, json_list
from app.api.api_master import *
from app.api.api_client import get_client_loves_master
from app.socket_io.journal_socketio import get_vacations_list, get_not_working_list, get_appointments_list


def fill_busy_time(master, date_obj):
    appointments = get_appointments_list(master['id'], date_obj)
    vacations = get_vacations_list(master['id'], date_obj)
    not_works = get_not_working_list(master['id'], date_obj)

    busy_time = appointments + vacations + not_works
    master['busyTime'] = busy_time


def set_favourite(master):
    if current_user.is_authenticated:
        if get_client_loves_master(current_user.id, master['id']):
            master['favourite'] = ''


@socketio.on('get_busy_time', namespace='/appointment')
def get_busy_time(data):
    try:
        date_obj = datetime.strptime(data['date'], '%d.%m.%Y')
        procedure_id = data['procedure']

        masters = json_list(get_masters_working_do_procedure_client_view(date_obj, procedure_id))

        for master in masters:
            fill_busy_time(master, date_obj)
            set_favourite(master)

        emit('get_busy_time', {'status': True,
                               'data': masters}, json=True)
    except ValueError:
        emit('get_busy_time', {'status': False,
                               'message': 'Некоректний формат часу'}, json=True)
