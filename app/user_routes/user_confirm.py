import pytz
from flask import url_for, redirect, request
from flask_login import login_required, current_user
import datetime

from app import app
from app.models import Appointment
from app.api.api_master import get_master, get_master_procedure_duration
from app.api.api_procedure import get_procedure
from app.api.api_appointment import add_appointment


def assert_master_exists(master_id):
    if get_master(master_id) is None:
        raise AssertionError('Не існує такого майстра')


def assert_procedure_exists(procedure_id):
    if get_procedure(procedure_id) is None:
        raise AssertionError('Не існує такої процедури')


def assert_duration_not_none(duration):
    if duration is None:
        raise AssertionError('Оберіть іншого майстра або процедуру')


def assert_start_mod(start):
    if start.minute % 30 != 0:
        raise AssertionError('Некоректний час, кожні 30хв')


def assert_start_future(start):
    start_tz = pytz.timezone('Europe/Kiev').localize(start)
    now = datetime.datetime.now(pytz.timezone('Europe/Kiev'))

    if start_tz <= now:
        raise AssertionError('Дата та час мають бути у майбутньому')


@app.route('/confirm', methods=['GET'])
@login_required
def confirm_get():
    try:
        if request.args.get('date') is None or \
                request.args.get('time') is None or \
                request.args.get('master') is None or \
                request.args.get('procedure') is None:
            raise AssertionError('Недостатньо параметрів')

        start = datetime.datetime.strptime(
            request.args.get('date') + ' ' + request.args.get('time'),
            '%d.%m.%Y %H:%M'
        )
        master_id = int(request.args.get('master'))
        procedure_id = int(request.args.get('procedure'))

        assert_master_exists(master_id)
        assert_procedure_exists(procedure_id)

        duration = get_master_procedure_duration(master_id, procedure_id)
        assert_duration_not_none(duration)

        assert_start_mod(start)
        assert_start_future(start)

        end = start + datetime.timedelta(minutes=duration)
        price = get_procedure(procedure_id).price_min

        appointment = Appointment(appoint_start=start, appoint_end=end,
                                  status=False, price=price,
                                  client_id=current_user.id, master_id=master_id, procedure_id=procedure_id)

        ok, message = add_appointment(appointment)

        if ok:
            return redirect(url_for('user_appointments_get', success=message))
        else:
            return redirect(url_for('user_appointments_get', error=message))

    except ValueError:
        return redirect(url_for('user_appointments_get', error='Некоректний формат'))
    except AssertionError as e:
        return redirect(url_for('user_appointments_get', error=e))
