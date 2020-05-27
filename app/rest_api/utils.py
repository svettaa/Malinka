import datetime
from decimal import Decimal

from flask import jsonify


def json_one(row, additional=dict()):
    if row is None:
        return None
    result = {}
    for item in row.items():
        if type(item[1]) == datetime.datetime:
            result[item[0]] = datetime.datetime.strftime(item[1], '%d.%m.%Y %H:%M')
        elif type(item[1]) == datetime.date:
            result[item[0]] = datetime.datetime.strftime(item[1], '%d.%m.%Y')
        elif type(item[1]) == Decimal:
            result[item[0]] = int(item[1])
        else:
            result[item[0]] = item[1]
    for part in additional.items():
        result[part[0]] = part[1]
    return result


def json_list(rows):
    if rows is None:
        return None
    return [json_one(row) for row in rows]


def build_form_invalid_reply(form):
    return jsonify({'status': False,
                    'message': next(iter(form.errors.values()))})


def build_list_data_reply(data):
    return jsonify({'status': True,
                    'data': json_list(data)})


def build_one_data_reply(data, additional=dict()):
    return jsonify({'status': True,
                    'data': json_one(data, additional)})


def build_message_reply(result):
    return jsonify({'status': result[0],
                    'message': str(result[1])})
