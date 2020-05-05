from app import db
from app.models import Master


def assert_master_is_hired(master: Master):
    pass
    # if master.is_hired:
    #     return
    # if db.session.execute('SELECT COUNT(*) '
    #                       'FROM Appointment '
    #                       'WHERE master_id = :master_id AND '
    #                       '      is_future_date_and_time(appoint_date, start_time);',
    #                       {'master_id': master.id}).scalar() > 0:
    #     raise AssertionError('Неможливо звільнити майстра, який має невиконані записи')


def assert_master_even_schedule(master: Master):
    pass
    # if db.session.execute('SELECT COUNT(*) '
    #                       'FROM Appointment INNER JOIN Master ON master_id = Master.id '
    #                       'WHERE master_id = :master_id '
    #                       '      AND '
    #                       '      is_future_date_and_time(appoint_date, start_time) '
    #                       '      AND'
    #                       '      is_even_day(appoint_date) <> :even_schedule;',
    #                       {'master_id': master.id,
    #                        'even_schedule': bool(master.even_schedule)}).scalar() > 0:
    #     raise AssertionError('Неможливо змінити графік майстра, існують невиконані записи за старим графіком')
