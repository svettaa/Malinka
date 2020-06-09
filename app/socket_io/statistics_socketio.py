from flask_login import login_required
from flask import request, jsonify
import datetime

from app import app
from app.login import admin_only
from app.socket_io import json_list
from app.db_api.statistics import *


@app.route('/get_base_statistics', methods=['GET'])
@login_required
@admin_only
def get_base_statistics():
    return jsonify({'status': False,
                    'data': {'users': get_users_amount(),
                             'masters': get_working_masters_amount()}})


@app.route('/get_interval_statistics', methods=['GET'])
@login_required
@admin_only
def get_interval_statistics():
    try:
        date_start_str = request.args.get('date_start')
        date_end_str = request.args.get('date_end')
        date_start = datetime.strptime(date_start_str, '%d.%m.%Y')
        date_end = datetime.strptime(date_end_str, '%d.%m.%Y')
        if date_start > date_end:
            return jsonify({'status': False,
                            'message': 'Дата початку не повинна бути більшою за дату кінця'})
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
            return jsonify({'status': True,
                            'data': data})
    except ValueError:
        return jsonify({'status': False,
                        'message': 'Некоректний формат часу'})
