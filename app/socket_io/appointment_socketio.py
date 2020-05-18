from datetime import timedelta

from dateutil.relativedelta import relativedelta
from flask_login import current_user
from flask import jsonify, request

from app import app, pytz
from app.socket_io import json_one, json_list
from app.api.api_master import *
from app.api.api_client import get_client_loves_master
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

    now = datetime.now(pytz.timezone('Europe/Kiev'))
    now_time = (now + timedelta(minutes=1)).strftime("%H:%M")
    if date_obj.date() == now.date():
        new_result = []
        for interval in result:
            if interval['end'] > now_time:
                interval['start'] = max(interval['start'], now_time)
                new_result.append(interval)
        result = new_result

    master['freeTime'] = result


def set_favourite(master):
    if current_user.is_authenticated:
        if get_client_loves_master(current_user.id, master['id']):
            master['favourite'] = ''


def assert_date_future_and_not_long(start):
    now = datetime.now(pytz.timezone('Europe/Kiev')).date()
    start_date = start.date()

    if start_date < now:
        raise AssertionError('Обрано дату у минулому')
    if start_date > now + relativedelta(months=2):
        raise AssertionError('Дозволено записуватися лише на 2 місяці вперед')


@app.route('/get_free_time', methods=['GET'])
def get_free_time():
    try:
        date_obj = datetime.strptime(request.args.get('date'), '%d.%m.%Y')
        procedure_id = request.args.get('procedure')

        assert_date_future_and_not_long(date_obj)

        masters = json_list(get_masters_working_do_procedure_client_view(date_obj, procedure_id))

        for master in masters:
            fill_free_time(master, date_obj)
            set_favourite(master)

        return jsonify({'status': True,
                        'data': masters})
    except ValueError:
        return jsonify({'status': False,
                        'message': 'Некоректний формат часу'})
    except AssertionError as e:
        return jsonify({'status': False,
                        'message': str(e)})
