from flask_socketio import emit
from flask_login import login_required
import datetime

from app import socketio
from app.login import admin_only
from app.socket_io import json_list
from app.api.api_statistics import *


@socketio.on('get_base_statistics', namespace='/statistics')
@login_required
@admin_only
def get_base_statistics():
    emit('get_base_statistics', {'status': False,
                                 'data': {'users': get_users_amount(),
                                          'masters': get_working_masters_amount()}}, json=True)


@socketio.on('get_interval_statistics', namespace='/statistics')
@login_required
@admin_only
def get_interval_statistics(dates):
    try:
        date_start = datetime.strptime(dates[0], '%d.%m.%Y')
        date_end = datetime.strptime(dates[1], '%d.%m.%Y')
        if date_start > date_end:
            emit('get_interval_statistics', {'status': False,
                                             'message': 'Дата початку не повинна бути більшою за дату кінця'},
                 json=True)
        else:
            data = {'appointments': get_interval_appointments_amount(date_start, date_end),
                    'money': int(get_interval_appointments_earned_money(date_start, date_end)),
                    'paints': int(get_interval_used_paints(date_start, date_end)),
                    'supplies': int(get_interval_supply_amount(date_start, date_end)),
                    'appointments-by-master': json_list(
                        get_interval_appointments_amount_by_master(date_start, date_end)),
                    'money-by-master': json_list(
                        get_interval_appointments_earned_money_by_master(date_start, date_end)),
                    'paints-by-paints': json_list(get_interval_used_paints_by_paints(date_start, date_end)),
                    'supplies-by-paints': json_list(get_interval_supply_amount_by_paints(date_start, date_end))}
            emit('get_interval_statistics', {'status': True,
                                             'data': data},
                 json=True)
    except ValueError:
        emit('get_interval_statistics', {'status': False,
                                         'message': 'Некоректний формат часу'}, json=True)
