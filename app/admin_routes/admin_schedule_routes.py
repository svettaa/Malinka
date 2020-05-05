from flask import render_template, request, redirect, url_for

from app import app
from app.models import *
from app.message_codes import *
from app.forms import AdminScheduleChangeForm
from app.api.api_schedule import *
from app.api.api_master import get_masters


@app.route('/schedules')
def schedules_get():
    return render_template('schedules.html', schedules=get_schedules(),
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/schedules/<int:schedule_id>', methods=['GET'])
def edit_schedule_get(schedule_id):
    schedule = get_schedule(schedule_id)
    form = AdminScheduleChangeForm(data=schedule)
    form.master_id.choices = [(str(schedule.master_id),
                               schedule.master_surname + ' ' + schedule.master_first_name)]
    form.master_id.render_kw = {'readonly': ''}

    return render_template('schedule.html', form=form,
                           action=url_for('edit_schedule_post', schedule_id=schedule_id))


@app.route('/schedules/<int:schedule_id>', methods=['POST'])
def edit_schedule_post(schedule_id):
    schedule = get_schedule(schedule_id)
    form = AdminScheduleChangeForm()
    form.master_id.choices = [(str(schedule.master_id),
                               schedule.master_surname + ' ' + schedule.master_first_name)]
    form.master_id.render_kw = {'readonly': ''}

    if not form.validate_on_submit():
        return render_template('schedule.html', form=form,
                               action=url_for('edit_schedule_post', schedule_id=schedule_id))

    schedule = ScheduleChange(id=schedule_id)
    form.populate_obj(schedule)

    status, message = update_schedule(schedule)

    if status:
        return redirect(url_for('schedules_get', success=Success.UPDATED_SCHEDULE.value))
    else:
        return render_template('schedule.html', form=form,
                               action=url_for('edit_schedule_post', schedule_id=schedule_id),
                               error=message)


@app.route('/schedules/new', methods=['GET'])
def new_schedule_get():
    form = AdminScheduleChangeForm()
    form.master_id.choices = [('', 'Не обрано')] + \
                             [(str(master['id']),
                               master['surname'] + ' ' + master['first_name'] + ', +38' + master['phone'])
                              for master in get_masters()]

    return render_template('schedule.html', form=form,
                           action=url_for('new_schedule_post'))


@app.route('/schedules/new', methods=['POST'])
def new_schedule_post():
    form = AdminScheduleChangeForm()
    form.master_id.choices = [('', 'Не обрано')] + \
                             [(str(master['id']),
                               master['surname'] + ' ' + master['first_name'] + ', +38' + master['phone'])
                              for master in get_masters()]

    if not form.validate_on_submit():
        return render_template('schedule.html', form=form,
                               action=url_for('new_schedule_post'))

    schedule = ScheduleChange()
    form.populate_obj(schedule)

    status, message = add_schedule(schedule)

    if status:
        return redirect(url_for('schedules_get', success=Success.ADDED_SCHEDULE.value))
    else:
        return render_template('schedule.html', form=form,
                               action=url_for('new_schedule_post'),
                               error=message)


@app.route('/schedules/delete/<int:schedule_id>', methods=['GET'])
def delete_schedule_get(schedule_id):
    status, message = delete_schedule(schedule_id)

    if status:
        return redirect(url_for('schedules_get', success=Success.DELETED_SCHEDULE.value))
    else:
        return redirect(url_for('schedules_get', error=Error.SCHEDULE_DELETE_INTEGRITY.value))
