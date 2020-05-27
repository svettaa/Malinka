import pytz
from flask import render_template, request, redirect, url_for
from flask_login import login_required

from app import app
from app.forms import AdminScheduleChangeForm
from app.api.api_schedule import *
from app.api.api_master import get_masters
from app.login import admin_only


@app.route('/schedules')
@login_required
@admin_only
def schedules_get():
    return render_template('schedules.html', schedules=get_schedules(), csrf_token=AdminScheduleChangeForm().csrf_token,
                           error=(request.args.get('error')),
                           success=(request.args.get('success')))


@app.route('/schedules/<int:schedule_id>', methods=['GET'])
@login_required
@admin_only
def edit_schedule_get(schedule_id):
    schedule = get_schedule(schedule_id)
    form = AdminScheduleChangeForm(data=schedule)
    form.master_id.choices = [(str(schedule.master_id),
                               schedule.master_surname + ' ' + schedule.master_first_name)]
    form.master_id.render_kw = {'readonly': ''}

    return render_template('schedule.html', form=form,
                           action=url_for('edit_schedule_post', schedule_id=schedule_id))


@app.route('/schedules/<int:schedule_id>', methods=['POST'])
@login_required
@admin_only
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
    schedule.change_start = pytz.timezone('Europe/Kiev').localize(schedule.change_start)
    schedule.change_end = pytz.timezone('Europe/Kiev').localize(schedule.change_end)

    status, message = update_schedule(schedule)

    if status:
        return redirect(url_for('schedules_get', success=message))
    else:
        return render_template('schedule.html', form=form,
                               action=url_for('edit_schedule_post', schedule_id=schedule_id),
                               error=message)


@app.route('/schedules/new', methods=['GET'])
@login_required
@admin_only
def new_schedule_get():
    form = AdminScheduleChangeForm()
    form.master_id.choices = [('', 'Не обрано')] + \
                             [(str(master['id']),
                               master['surname'] + ' ' + master['first_name'] + ', +38' + master['phone'])
                              for master in get_masters()]

    return render_template('schedule.html', form=form,
                           action=url_for('new_schedule_post'))


@app.route('/schedules/new', methods=['POST'])
@login_required
@admin_only
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
    schedule.change_start = pytz.timezone('Europe/Kiev').localize(schedule.change_start)
    schedule.change_end = pytz.timezone('Europe/Kiev').localize(schedule.change_end)

    status, message = add_schedule(schedule)

    if status:
        return redirect(url_for('schedules_get', success=message))
    else:
        return render_template('schedule.html', form=form,
                               action=url_for('new_schedule_post'),
                               error=message)


@app.route('/schedules/delete/<int:schedule_id>', methods=['GET'])
@login_required
@admin_only
def delete_schedule_get(schedule_id):
    status, message = delete_schedule(schedule_id)

    if status:
        return redirect(url_for('schedules_get', success=message))
    else:
        return redirect(url_for('schedules_get', error=message))
