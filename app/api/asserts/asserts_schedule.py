from sqlalchemy.orm import Session

from app import db
from app.models import ScheduleChange


def assert_schedule_no_overlaps(schedule: ScheduleChange, session: Session):
    if session.execute(""" SELECT COUNT(*)
                              FROM Schedule_Change
                              WHERE master_id = :master_id AND
                                    (change_start, change_end) 
                                    OVERLAPS
                                    (:change_start, :change_end);
                          """,
                       {'master_id': schedule.master_id,
                        'change_start': schedule.change_start,
                        'change_end': schedule.change_end}).scalar() > 1:
        raise AssertionError('Зміни в графіку не можуть перетинатися')


def assert_schedule_working_or_even_schedule(schedule: ScheduleChange, session: Session):
    future_dates = session.execute('SELECT appoint_start '
                                   'FROM Appointment '
                                   'WHERE master_id = :master_id AND '
                                   '      appoint_start > now() AND '
                                   '      NOT EXISTS (SELECT * '
                                   '                  FROM Schedule_Change '
                                   '                  WHERE Schedule_Change.master_id = Appointment.master_id '
                                   '                        AND is_working = True AND '
                                   '                        change_start <= appoint_start AND '
                                   '                        change_end >= appoint_end);',
                                   {'master_id': schedule.master_id}).fetchall()
    for future_date in future_dates:
        day = future_date.appoint_start.day
        even_day = (day % 2 == 0)
        master_even_schedule = session.execute('SELECT even_schedule '
                                               'FROM Master '
                                               'WHERE id = :master_id;',
                                               {'master_id': schedule.master_id}).scalar()
        if even_day != master_even_schedule:
            raise AssertionError('Неможливо змінити графік майстра, з\'являться записи не за графіком')


def assert_schedule_no_vacation_appointment(schedule: ScheduleChange, session: Session):
    if schedule.is_working:
        return
    if session.execute('SELECT COUNT(*) '
                       'FROM Appointment '
                       'WHERE master_id = :master_id AND '
                       '      (:change_start, :change_end) '
                       '      OVERLAPS '
                       '      (appoint_start, appoint_end);',
                       {'master_id': schedule.master_id,
                        'change_start': schedule.change_start,
                        'change_end': schedule.change_end}).scalar() > 0:
        raise AssertionError('У майстра є записи на цей час, не можна додати відпустку')
