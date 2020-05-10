from datetime import datetime


def json_one(row):
    if row is None:
        return None
    result = {}
    for item in row.items():
        if type(item[1]) == datetime:
            result[item[0]] = datetime.strftime(item[1], '%d.%m.%Y %H:%M')
        else:
            result[item[0]] = item[1]
    return result


def json_list(rows):
    if rows is None:
        return None
    return [json_one(row) for row in rows]


from app.socket_io.master_socketio import *
