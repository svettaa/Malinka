from flask_socketio import emit
from flask_login import login_required, current_user
from datetime import datetime

from app import socketio
from app.login import master_only
from app.socket_io import json_one, json_list
from app.api.api_appointment import get_master_date_appointments


@socketio.on('get_master_timetable', namespace='/master')
@login_required
@master_only
def get_master_timetable(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d.%m.%Y')
        timetable = get_master_date_appointments(current_user.id, date_obj)
        emit('get_master_timetable', {'status': True,
                                      'data': json_list(timetable)}, json=True)
    except ValueError:
        emit('get_master_timetable', {'status': False,
                                      'message': 'Некоректний формат часу'}, json=True)
