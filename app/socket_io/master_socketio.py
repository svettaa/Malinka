from flask_login import login_required, current_user
from datetime import datetime
from flask import jsonify, request

from app import app
from app.login import master_only
from app.socket_io import json_one, json_list
from app.api.api_appointment import get_master_date_appointments
from app.socket_io.journal_socketio import get_vacations_list, get_not_working_list


@app.route('/get_master_timetable', methods=['GET'])
@login_required
@master_only
def get_master_timetable():
    try:
        date_obj = datetime.strptime(request.args.get('date'), '%d.%m.%Y')
        master = {'appointments': json_list(get_master_date_appointments(current_user.id, date_obj)),
                  'vacations': get_vacations_list(current_user.id, date_obj),
                  'notWorking': get_not_working_list(current_user.id, date_obj)}
        return jsonify({'status': True,
                        'data': master})
    except ValueError:
        return jsonify({'status': False,
                        'message': 'Некоректний формат часу'})
