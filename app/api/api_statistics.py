from datetime import datetime

from app import db


def get_users_amount():
    return db.engine.execute('SELECT COUNT(*) '
                             'FROM Client;').scalar()


def get_working_masters_amount():
    return db.engine.execute('SELECT COUNT(*) '
                             'FROM Master '
                             'WHERE is_hired = True;').scalar()


def get_interval_appointments_amount(date_start: datetime, date_end: datetime):
    return db.engine.execute('SELECT COUNT(*) '
                             'FROM Appointment '
                             'WHERE Date(appoint_start) BETWEEN %s AND %s',
                             (date_start, date_end)).scalar()


def get_interval_appointments_earned_money(date_start: datetime, date_end: datetime):
    return db.engine.execute('SELECT COALESCE(SUM(price), 0) '
                             'FROM Appointment '
                             'WHERE (Date(appoint_start) BETWEEN %s AND %s) AND '
                             '      appoint_end <= now()',
                             (date_start, date_end)).scalar()


def get_interval_used_paints(date_start: datetime, date_end: datetime):
    return db.engine.execute('SELECT COALESCE(SUM(volume_ml), 0) '
                             'FROM Appointment INNER JOIN Appointment_Paint '
                             '     ON Appointment.id = appointment_id '
                             'WHERE (Date(appoint_start) BETWEEN %s AND %s);',
                             (date_start, date_end)).scalar()


def get_interval_supply_amount(date_start: datetime, date_end: datetime):
    return db.engine.execute('SELECT COALESCE(SUM(amount), 0) '
                             'FROM Paint_Supply '
                             'WHERE supply_date BETWEEN %s AND %s;',
                             (date_start, date_end)).scalar()


def get_interval_appointments_amount_by_master(date_start: datetime, date_end: datetime):
    return db.engine.execute('SELECT surname, first_name, '
                             '       (SELECT COUNT(*)'
                             '        FROM Appointment '
                             '        WHERE (Date(appoint_start) BETWEEN %s AND %s) AND '
                             '               master_id = Master.id) '
                             '        AS amount '
                             'FROM Master INNER JOIN Client ON Master.id = Client.id '
                             'ORDER BY surname, first_name;',
                             (date_start, date_end)).fetchall()


def get_interval_appointments_earned_money_by_master(date_start: datetime, date_end: datetime):
    return db.engine.execute('SELECT surname, first_name, '
                             '       (SELECT COALESCE(SUM(price), 0) '
                             '        FROM Appointment '
                             '        WHERE (Date(appoint_start) BETWEEN %s AND %s) AND '
                             '               master_id = Master.id AND appoint_end <= now() '
                             '        ) AS sum_price '
                             'FROM Master INNER JOIN Client ON Master.id = Client.id '
                             'ORDER BY surname, first_name;',
                             (date_start, date_end)).fetchall()


def get_interval_used_paints_by_paints(date_start: datetime, date_end: datetime):
    return db.engine.execute('SELECT code, name, COALESCE(SUM(volume_ml), 0) AS amount '
                             'FROM (Appointment INNER JOIN Appointment_Paint '
                             '     ON Appointment.id = appointment_id) INNER JOIN Paint '
                             '     ON paint_id = Paint.id '
                             'WHERE (Date(appoint_start) BETWEEN %s AND %s) '
                             'GROUP BY code, name '
                             'ORDER BY code, name;',
                             (date_start, date_end)).fetchall()


def get_interval_supply_amount_by_paints(date_start: datetime, date_end: datetime):
    return db.session.execute('SELECT code, name, SUM(amount) AS amount '
                              'FROM Paint_Supply INNER JOIN Paint '
                              '     ON paint_id = Paint.id '
                              'WHERE (supply_date BETWEEN :date_start AND :date_end) '
                              'GROUP BY code, name '
                              'ORDER BY code, name;',
                              {'date_start': date_start,
                               'date_end': date_end}).fetchall()
