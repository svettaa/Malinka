from flask import render_template, request, redirect, url_for
from flask_login import login_required

from app import app
from app.message_codes import *
from app.forms import AdminPaintForm
from app.api.api_paint import *
from app.login import admin_only


@app.route('/paints', methods=['GET'])
@login_required
@admin_only
def paints_get():
    return render_template('paints.html', paints=get_paints(),
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/paints/<int:paint_id>', methods=['GET'])
@login_required
@admin_only
def edit_paint_get(paint_id):
    form = AdminPaintForm(data=get_paint(paint_id))

    return render_template('paint.html', form=form,
                           action=url_for('edit_paint_post', paint_id=paint_id))


@app.route('/paints/<int:paint_id>', methods=['POST'])
@login_required
@admin_only
def edit_paint_post(paint_id):
    form = AdminPaintForm()

    if not form.validate_on_submit():
        return render_template('paint.html', form=form,
                               action=url_for('edit_paint_post', paint_id=paint_id))

    paint = Paint(id=paint_id)
    form.populate_obj(paint)

    status, message = update_paint(paint)

    if status:
        return redirect(url_for('paints_get', success=Success.UPDATED_PAINT.value))
    else:
        return render_template('paint.html', form=form,
                               action=url_for('edit_paint_post', paint_id=paint_id),
                               error=message)


@app.route('/paints/new', methods=['GET'])
@login_required
@admin_only
def new_paint_get():
    form = AdminPaintForm()

    return render_template('paint.html', form=form,
                           action=url_for('new_paint_post'))


@app.route('/paints/new', methods=['POST'])
@login_required
@admin_only
def new_paint_post():
    form = AdminPaintForm()

    if not form.validate_on_submit():
        return render_template('paint.html', form=form,
                               action=url_for('new_paint_post'))

    paint = Paint()
    form.populate_obj(paint)

    status, message = add_paint(paint)

    if status:
        return redirect(url_for('paints_get', success=Success.ADDED_PAINT.value))
    else:
        return render_template('paint.html', form=form,
                               action=url_for('new_paint_post'),
                               error=message)


@app.route('/paints/delete/<int:paint_id>', methods=['GET'])
@login_required
@admin_only
def delete_paint_get(paint_id):

    status, message = delete_paint(paint_id)

    if status:
        return redirect(url_for('paints_get', success=Success.DELETED_PAINT.value))
    else:
        return redirect(url_for('paints_get',
                                error=Error.PAINT_HAS_APPOINTMENTS.value))
