from sqlalchemy.orm import Session
from app.models import Master


def assert_master_is_hired(master: Master, session: Session):
    if master.is_hired:
        return
    if session.execute('SELECT COUNT(*) '
                       'FROM Appointment '
                       'WHERE master_id = :master_id AND '
                       '      appoint_start > now();',
                       {'master_id': master.id}).scalar() > 0:
        raise AssertionError('Неможливо звільнити майстра, який має невиконані записи')


def assert_master_even_schedule_or_working(master: Master, session: Session):
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
                                   {'master_id': master.id}).fetchall()
    for future_date in future_dates:
        day = future_date.appoint_start.day
        even_day = (day % 2 == 0)
        if even_day != master.even_schedule:
            raise AssertionError('Неможливо змінити графік майстра, існують невиконані записи за старим графіком '
                                 '(можна додати понаднормові години)')


def assert_master_procedures(master: Master, session: Session):
    if session.execute('SELECT COUNT(*) '
                       'FROM Appointment '
                       'WHERE master_id = :master_id AND '
                       '      appoint_start > now() AND '
                       '      NOT EXISTS (SELECT * '
                       '                  FROM Master_Procedure '
                       '                  WHERE Master_Procedure.master_id = Appointment.master_id AND'
                       '                        Master_Procedure.procedure_id = Appointment.procedure_id)',
                       {'master_id': master.id}).scalar() > 0:
        raise AssertionError('У майстра є невиконані записи з процедурою, яку намагаєтесь видалити')
