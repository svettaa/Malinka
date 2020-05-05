from app import db
from app.models import ScheduleChange


def assert_schedule_overlapping(schedule: ScheduleChange):
    if db.session.execute(""" SELECT COUNT(*)
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
