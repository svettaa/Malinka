from app import db
from app.models import ScheduleChange


def assert_schedule_overlapping(schedule: ScheduleChange):
    if db.session.execute(""" SELECT *
                              FROM Schedule_Change SC1 
                              WHERE SC1.master_id = :master_id AND
                                    EXISTS (
                                       SELECT *
                                       FROM Schedule_Change SC2 
                                       WHERE SC2.master_id = :master_id AND
                                             SC2.id <> SC1.id AND
                                               (SC1.change_start, SC1.change_end) 
                                               OVERLAPS
                                               (SC2.change_start, SC2.change_end)
                                    );
                          """,
                          {'master_id': schedule.master_id}).scalar() is not None:
        raise AssertionError('Зміни в графіку не можуть перетинатися')
