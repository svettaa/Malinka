from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError, DataError

from app import app
from app.models import *
from app.message_codes import *


@app.route('/supplies')
def supplies_get():
    supplies = db.engine.execute('SELECT Paint.code AS paint_code, Paint.name AS paint_name, '
                                 '       supply_date, amount, Paint_Supply.id AS id '
                                 'FROM Paint INNER JOIN Paint_Supply '
                                 '     ON Paint.id = Paint_Supply.paint_id '
                                 'ORDER BY supply_date DESC').fetchall()

    return render_template('supplies.html', supplies=supplies,
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/supplies/<int:supply_id>', methods=['GET'])
def edit_supply_get(supply_id):
    supply = db.engine.execute('SELECT id, paint_id, supply_date, amount '
                               'FROM Paint_Supply '
                               'WHERE id = %s;',
                               supply_id).fetchone()

    paints = db.engine.execute('SELECT id, code, name '
                               'FROM Paint').fetchall()

    return render_template('supply.html', supply=supply, paints=paints,
                           action=url_for('edit_supply_post', supply_id=supply_id))


@app.route('/supplies/<int:supply_id>', methods=['POST'])
def edit_supply_post(supply_id):
    supply = PaintSupply(id=supply_id, paint_id=request.form['supplyPaint'],
                         amount=request.form['supplyHowMuch'], supply_date=request.form['supplyDate'])

    try:
        old_amount = db.engine.execute('SELECT amount '
                                       'FROM Paint_Supply '
                                       'WHERE id = %s;',
                                       supply_id).fetchone()['amount']
        db.engine.execute('UPDATE Paint_Supply '
                          'SET paint_id = %s,'
                          '    amount = %s,'
                          '    supply_date = %s '
                          'WHERE id = %s;',
                          (supply.paint_id, supply.amount,
                           supply.supply_date, supply.id))

        db.engine.execute('UPDATE Paint '
                          'SET left_ml = left_ml - %s '
                          'WHERE id = %s',
                          (old_amount, supply.paint_id))
        db.engine.execute('UPDATE Paint '
                          'SET left_ml = left_ml + %s '
                          'WHERE id = %s',
                          (supply.amount, supply.paint_id))
    except (DataError, IntegrityError):

        paints = db.engine.execute('SELECT id, code, name '
                                   'FROM Paint').fetchall()
        return render_template('supply.html', supply=supply, paints=paints,
                               action=url_for('edit_supply_post', supply_id=supply_id),
                               error=get_error_message(Error.SUPPLY_ILLEGAL_DATA.value))

    return redirect(url_for('supplies_get', success=Success.UPDATED_SUPPLY.value))


@app.route('/supplies/new', methods=['GET'])
def new_supply_get():
    paints = db.engine.execute('SELECT id, code, name '
                               'FROM Paint').fetchall()

    return render_template('supply.html', supply=None, paints=paints,
                           action=url_for('new_supply_post'))


@app.route('/supplies/new', methods=['POST'])
def new_supply_post():
    supply = PaintSupply(paint_id=request.form['supplyPaint'],
                         amount=request.form['supplyHowMuch'], supply_date=request.form['supplyDate'])

    try:
        db.engine.execute('INSERT INTO Paint_Supply (paint_id, amount, supply_date) '
                          'VALUES (%s, %s, %s);',
                          (supply.paint_id, supply.amount, supply.supply_date))
        db.engine.execute('UPDATE Paint '
                          'SET left_ml = left_ml + %s '
                          'WHERE id = %s',
                          (supply.amount, supply.paint_id))
    except (DataError, IntegrityError):

        paints = db.engine.execute('SELECT id, code, name '
                                   'FROM Paint').fetchall()
        return render_template('supply.html', supply=supply, paints=paints,
                               action=url_for('new_supply_post'),
                               error=get_error_message(Error.SUPPLY_ILLEGAL_DATA.value))

    return redirect(url_for('supplies_get', success=Success.ADDED_SUPPLY.value))


@app.route('/supplies/delete/<int:supply_id>', methods=['GET'])
def delete_supply_get(supply_id):
    old = db.engine.execute('SELECT amount, paint_id '
                            'FROM Paint_Supply '
                            'WHERE id = %s;',
                            supply_id).fetchone()
    db.engine.execute('DELETE '
                      'FROM Paint_Supply '
                      'WHERE id = %s',
                      supply_id)
    db.engine.execute('UPDATE Paint '
                      'SET left_ml = left_ml - %s '
                      'WHERE id = %s',
                      (old['amount'], old['paint_id']))

    return redirect(url_for('supplies_get', success=Success.DELETED_SUPPLY.value))
