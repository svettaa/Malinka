from flask_socketio import emit
from flask_login import login_required
from datetime import datetime

from app import socketio
from app.login import master_only
from app.socket_io import json_one, json_list
from app.api.api_appointment import get_master_date_appointments
from app.api.api_master import get_masters_working


@socketio.on('get_journal', namespace='/admin')
@login_required
@master_only
def get_journal(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d.%m.%Y')

        masters = json_list(get_masters_working(date_obj))

        for master in masters:
            master['appointments'] = json_list(get_master_date_appointments(master['id'], date_obj))

        emit('get_journal', {'status': True,
                             'data': masters}, json=True)
    except ValueError:
        emit('get_journal', {'status': False,
                             'message': 'Некоректний формат часу'}, json=True)
