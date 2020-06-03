from sqlalchemy.exc import IntegrityError, OperationalError

from app import db
from app.api.utils import *
from app.api.asserts.asserts_schedule import *


def get_schedules():
    return db.engine.execute('SELECT Schedule_Change.id, surname, first_name, phone, '
                             '       change_start, change_end, is_working '
                             'FROM (Schedule_Change INNER JOIN Master '
                             '     ON Schedule_Change.master_id = Master.id) INNER JOIN Client '
                             '     ON Master.id = Client.id '
                             'ORDER BY change_start DESC').fetchall()


def get_schedule(schedule_id: int):
    return db.engine.execute('SELECT Schedule_Change.id, master_id, '
                             '       change_start, change_end, is_working,'
                             '       surname AS master_surname, first_name AS master_first_name '
                             'FROM (Schedule_Change INNER JOIN Master '
                             '     ON Schedule_Change.master_id = Master.id) INNER JOIN Client '
                             '     ON Master.id = Client.id '
                             'WHERE Schedule_Change.id = %s;',
                             schedule_id).fetchone()


def update_schedule(schedule: ScheduleChange):
    if schedule.change_start >= schedule.change_end:
        return False, 'Початкова дата має бути меньшою за кінцеву'
    if int(schedule.master_id) != get_schedule(schedule.id).master_id:
        return False, 'Не можна змінювати майстра у зміні графіку'

    session = get_serializable_session()
    try:
        assert_schedule_matters(schedule, session)
        session.execute('UPDATE Schedule_Change '
                        'SET change_start = :change_start,'
                        '    change_end = :change_end, '
                        '    is_working = :is_working,'
                        '    master_id = :master_id '
                        'WHERE id = :id',
                        {'change_start': schedule.change_start,
                         'change_end': schedule.change_end,
                         'is_working': bool(schedule.is_working),
                         'master_id': schedule.master_id,
                         'id': schedule.id})
        assert_schedule_no_overlaps(schedule, session)
        assert_schedule_working_or_even_schedule(schedule, session)
        assert_schedule_no_vacation_appointment(schedule, session)
        session.commit()
        return True, 'Успішно оновлено зміну в графіку'
    except IntegrityError:
        session.rollback()
        return False, ''
    except AssertionError as e:
        session.rollback()
        return False, e
    except OperationalError:
        session.rollback()
        return update_schedule(schedule)
    finally:
        session.close()


def add_schedule(schedule: ScheduleChange):
    if schedule.change_start >= schedule.change_end:
        return False, 'Початкова дата має бути меньшою за кінцеву'

    session = get_serializable_session()
    try:
        assert_schedule_matters(schedule, session)
        session.execute('INSERT INTO Schedule_Change (change_start, change_end, is_working, master_id) '
                        'VALUES (:change_start, :change_end, :is_working, :master_id);',
                        {'change_start': schedule.change_start,
                         'change_end': schedule.change_end,
                         'is_working': bool(schedule.is_working),
                         'master_id': schedule.master_id})
        assert_schedule_no_overlaps(schedule, session)
        assert_schedule_no_vacation_appointment(schedule, session)
        session.commit()
        return True, 'Успішно додано зміну в графіку'
    except IntegrityError:
        session.rollback()
        return False, ''
    except AssertionError as e:
        session.rollback()
        return False, e
    except OperationalError:
        session.rollback()
        return add_schedule(schedule)
    finally:
        session.close()


def delete_schedule(schedule_id: int):
    session = get_serializable_session()
    try:
        session.execute('DELETE FROM Schedule_Change '
                        'WHERE id = :id',
                        {'id': schedule_id})
        assert_schedule_working_or_even_schedule(get_schedule(schedule_id), session)
        session.commit()
        return True, 'Успішно видалено зміну в графіку'
    except IntegrityError:
        session.rollback()
        return False, ''
    except AssertionError as e:
        session.rollback()
        return False, e
    except OperationalError:
        session.rollback()
        return delete_schedule(schedule_id)
    finally:
        session.close()
