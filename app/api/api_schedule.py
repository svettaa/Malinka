from sqlalchemy.exc import IntegrityError

from app import db
from app.models import ScheduleChange


def get_schedules():
    return db.engine.execute('SELECT Schedule_Change.id, surname, first_name, phone, '
                             '       change_start, change_end, is_working '
                             'FROM (Schedule_Change INNER JOIN Master '
                             '     ON Schedule_Change.master_id = Master.id) INNER JOIN Client '
                             '     ON Master.id = Client.id '
                             'ORDER BY change_start DESC').fetchall()


def get_schedule(schedule_id: int):
    return db.engine.execute('SELECT Schedule_Change.id, master_id, '
                             '       change_start, change_end, is_working '
                             'FROM (Schedule_Change INNER JOIN Master '
                             '     ON Schedule_Change.master_id = Master.id) INNER JOIN Client '
                             '     ON Master.id = Client.id '
                             'WHERE Schedule_Change.id = %s;',
                             schedule_id).fetchone()


def update_schedule(schedule: ScheduleChange):
    try:
        db.engine.execute('UPDATE Schedule_Change '
                          'SET change_start = %s,'
                          '    change_end = %s, '
                          '    is_working = %s,'
                          '    master_id = %s '
                          'WHERE id = %s',
                          (schedule.change_start, schedule.change_end, bool(schedule.is_working),
                           schedule.master_id, schedule.id))
        return True, 'Успішно оновлено зміну в графіку'
    except IntegrityError:
        return False, ''


def add_schedule(schedule: ScheduleChange):
    try:
        db.engine.execute('INSERT INTO Schedule_Change (change_start, change_end, is_working, master_id) '
                          'VALUES (%s, %s, %s, %s)',
                          (schedule.change_start, schedule.change_end, bool(schedule.is_working), schedule.master_id))
        return True, 'Успішно додано зміну в графіку'
    except IntegrityError:
        return False, ''


def delete_schedule(schedule_id: int):
    try:
        db.engine.execute('DELETE FROM Schedule_Change '
                          'WHERE id = %s',
                          schedule_id)
        return True, 'Успішно видалено зміну в графіку'
    except IntegrityError:
        return False, ''
