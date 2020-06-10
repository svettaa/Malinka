from sqlalchemy.orm import Session
from app.models import Procedure


def assert_procedure_is_relevant(procedure: Procedure, session: Session):
    if procedure.is_relevant:
        return
    if session.execute('SELECT COUNT(*) '
                       'FROM Appointment '
                       'WHERE procedure_id = :procedure_id AND '
                       '      appoint_start > now();',
                       {'procedure_id': procedure.id}).scalar() > 0:
        raise AssertionError('Неможливо зробити процедуру неактуальною, існують невиконані записи')


def assert_procedure_uses_paints(procedure: Procedure, session: Session):
    if procedure.uses_paints:
        return
    if session.execute('SELECT COUNT(*) '
                       'FROM Appointment  '
                       'WHERE procedure_id = :procedure_id AND '
                       '      EXISTS (SELECT * '
                       '              FROM Appointment_Paint '
                       '              WHERE Appointment.id = appointment_id);',
                       {'procedure_id': procedure.id}).scalar() > 0:
        raise AssertionError('Неможливо зробити процедуру такою, що не використовує фарби, існують записи '
                             'з даною процедурою, що використовують фарби')
