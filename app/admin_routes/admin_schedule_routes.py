from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError, DataError

from app import app
from app.models import *
from app.message_codes import *
from app.forms import AdminScheduleChangeForm


@app.route('/schedules')
def schedules_get():
    schedules = db.engine.execute('SELECT Schedule_Change.id, surname, first_name, phone, '
                                  '       change_start, change_end, is_working '
                                  'FROM (Schedule_Change INNER JOIN Master '
                                  '     ON Schedule_Change.master_id = Master.id) INNER JOIN Client '
                                  '     ON Master.id = Client.id '
                                  'ORDER BY change_start DESC').fetchall()

    return render_template('schedules.html', schedules=schedules,
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/schedules/<int:schedule_id>', methods=['GET'])
def edit_schedule_get(schedule_id):
    schedule = db.engine.execute('SELECT Schedule_Change.id, master_id, '
                                 '       change_start, change_end, is_working '
                                 'FROM (Schedule_Change INNER JOIN Master '
                                 '     ON Schedule_Change.master_id = Master.id) INNER JOIN Client '
                                 '     ON Master.id = Client.id '
                                 'WHERE Schedule_Change.id = %s;',
                                 schedule_id).fetchone()

    masters = db.engine.execute('SELECT Master.id, surname, first_name, phone '
                                'FROM Master INNER JOIN Client '
                                '     ON Master.id = Client.id;').fetchall()

    form = AdminScheduleChangeForm(data=schedule)
    form.master_id.choices = [
        (master['id'], master['surname'] + ' ' + master['first_name'] + ', +38' + master['phone'])
        for master in masters]

    return render_template('schedule.html', form=form,
                           action=url_for('edit_schedule_post', schedule_id=schedule_id))


@app.route('/schedules/<int:schedule_id>', methods=['POST'])
def edit_schedule_post(schedule_id):
    form = AdminScheduleChangeForm()

    masters = db.engine.execute('SELECT Master.id, surname, first_name, phone '
                                'FROM Master INNER JOIN Client '
                                '     ON Master.id = Client.id;').fetchall()
    form.master_id.choices = [
        (master['id'], master['surname'] + ' ' + master['first_name'] + ', +38' + master['phone'])
        for master in masters]

    if not form.validate_on_submit():
        return render_template('schedule.html', form=form,
                               action=url_for('edit_schedule_post', schedule_id=schedule_id))

    schedule = ScheduleChange(id=schedule_id)
    form.populate_obj(schedule)

    try:
        db.engine.execute('UPDATE Schedule_Change '
                          'SET change_start = %s,'
                          '    change_end = %s, '
                          '    is_working = %s,'
                          '    master_id = %s '
                          'WHERE id = %s',
                          (schedule.change_start, schedule.change_end, bool(schedule.is_working),
                           schedule.master_id, schedule.id))
    except IntegrityError:
        return render_template('schedule.html', form=form,
                               action=url_for('edit_schedule_post', schedule_id=schedule_id),
                               error=Error.SCHEDULE_INTEGRITY)

    return redirect(url_for('schedules_get', success=Success.UPDATED_SCHEDULE.value))


@app.route('/schedules/new', methods=['GET'])
def new_schedule_get():
    masters = db.engine.execute('SELECT Master.id, surname, first_name, phone '
                                'FROM Master INNER JOIN Client '
                                '     ON Master.id = Client.id;').fetchall()

    form = AdminScheduleChangeForm()
    form.master_id.choices = [
        (master['id'], master['surname'] + ' ' + master['first_name'] + ', +38' + master['phone'])
        for master in masters]

    return render_template('schedule.html', form=form,
                           action=url_for('new_schedule_post'))


@app.route('/schedules/new', methods=['POST'])
def new_schedule_post():
    form = AdminScheduleChangeForm()

    masters = db.engine.execute('SELECT Master.id, surname, first_name, phone '
                                'FROM Master INNER JOIN Client '
                                '     ON Master.id = Client.id;').fetchall()
    form.master_id.choices = [
        (master['id'], master['surname'] + ' ' + master['first_name'] + ', +38' + master['phone'])
        for master in masters]

    if not form.validate_on_submit():
        return render_template('schedule.html', form=form,
                               action=url_for('new_schedule_post'))

    schedule = ScheduleChange()
    form.populate_obj(schedule)

    try:
        db.engine.execute('INSERT INTO Schedule_Change (change_start, change_end, is_working, master_id) '
                          'VALUES (%s, %s, %s, %s)',
                          (schedule.change_start, schedule.change_end, bool(schedule.is_working), schedule.master_id))
    except IntegrityError:
        return render_template('schedule.html', form=form,
                               action=url_for('new_schedule_post'),
                               error=Error.SCHEDULE_INTEGRITY)

    return redirect(url_for('schedules_get', success=Success.ADDED_SCHEDULE.value))


@app.route('/schedules/delete/<int:schedule_id>', methods=['GET'])
def delete_schedule_get(schedule_id):
    try:
        db.engine.execute('DELETE FROM Schedule_Change '
                          'WHERE id = %s',
                          schedule_id)
    except IntegrityError:
        return redirect(url_for('schedules_get', error=Error.SCHEDULE_DELETE_INTEGRITY.value))

    return redirect(url_for('schedules_get', success=Success.DELETED_SCHEDULE.value))
