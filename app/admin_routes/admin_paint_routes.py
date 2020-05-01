from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError, DataError

from app import app
from app.models import *
from app.message_codes import *
from app.forms import AdminPaintForm


@app.route('/paints', methods=['GET'])
def paints_get():
    paints = db.engine.execute('SELECT id, code, name, left_ml '
                               'FROM Paint;').fetchall()

    return render_template('paints.html', paints=paints,
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/paints/<int:paint_id>', methods=['GET'])
def edit_paint_get(paint_id):
    paint = db.engine.execute('SELECT id, code, name, left_ml '
                              'FROM Paint '
                              'WHERE id = %s;',
                              paint_id).fetchone()

    form = AdminPaintForm(data=paint)

    return render_template('paint.html', form=form,
                           action=url_for('edit_paint_post', paint_id=paint_id))


@app.route('/paints/<int:paint_id>', methods=['POST'])
def edit_paint_post(paint_id):
    form = AdminPaintForm()

    if not form.validate_on_submit():
        return render_template('paint.html', form=form,
                               action=url_for('edit_paint_post', paint_id=paint_id))

    paint = Paint(id=paint_id)
    form.populate_obj(paint)

    try:
        db.engine.execute('UPDATE Paint '
                          'SET code = %s,'
                          '    name = %s '
                          'WHERE id = %s;',
                          (paint.code, paint.name, paint.id))
    except IntegrityError:
        return render_template('paint.html', form=form,
                               action=url_for('edit_paint_post', paint_id=paint_id),
                               error=get_error_message(Error.PAINT_CODE_EXISTS.value))

    return redirect(url_for('paints_get', success=Success.UPDATED_PAINT.value))


@app.route('/paints/new', methods=['GET'])
def new_paint_get():
    form = AdminPaintForm()

    return render_template('paint.html', form=form,
                           action=url_for('new_paint_post'))


@app.route('/paints/new', methods=['POST'])
def new_paint_post():
    form = AdminPaintForm()

    if not form.validate_on_submit():
        return render_template('paint.html', form=form,
                               action=url_for('new_paint_post'))

    paint = Paint()
    form.populate_obj(paint)

    try:
        db.engine.execute('INSERT INTO Paint (code, name, left_ml) '
                          'VALUES (%s, %s, %s);',
                          (paint.code, paint.name, 0))
    except IntegrityError:
        return render_template('paint.html', form=form,
                               action=url_for('new_paint_post'),
                               error=get_error_message(Error.PAINT_CODE_EXISTS.value))

    return redirect(url_for('paints_get', success=Success.ADDED_PAINT.value))


@app.route('/paints/delete/<int:paint_id>', methods=['GET'])
def delete_paint_get(paint_id):
    try:
        db.engine.execute('DELETE '
                          'FROM Paint '
                          'WHERE id = %s',
                          paint_id)
    except IntegrityError:
        return redirect(url_for('paints_get',
                                error=Error.PAINT_HAS_APPOINTMENTS.value))

    return redirect(url_for('paints_get', success=Success.DELETED_PAINT.value))
