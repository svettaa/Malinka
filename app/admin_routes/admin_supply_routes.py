from flask import render_template, request, redirect, url_for
from flask_login import login_required

from app import app
from app.models import *
from app.message_codes import *
from app.forms import AdminSupplyForm
from app.api.api_supply import *
from app.api.api_paint import get_paints
from app.login import admin_only


@app.route('/supplies')
@login_required
@admin_only
def supplies_get():
    return render_template('supplies.html', supplies=get_supplies(),
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/supplies/<int:supply_id>', methods=['GET'])
@login_required
@admin_only
def edit_supply_get(supply_id):
    supply = get_supply(supply_id)
    form = AdminSupplyForm(data=supply)
    form.paint_id.choices = [(str(supply.paint_id),
                             supply.paint_code + ' - ' + supply.paint_name)]
    form.paint_id.render_kw = {'readonly': ''}

    return render_template('supply.html', form=form,
                           action=url_for('edit_supply_post', supply_id=supply_id))


@app.route('/supplies/<int:supply_id>', methods=['POST'])
@login_required
@admin_only
def edit_supply_post(supply_id):
    supply = get_supply(supply_id)
    form = AdminSupplyForm()
    form.paint_id.choices = [(str(supply.paint_id),
                             supply.paint_code + ' - ' + supply.paint_name)]
    form.paint_id.render_kw = {'readonly': ''}

    if not form.validate_on_submit():
        return render_template('supply.html', form=form,
                               action=url_for('edit_supply_post', supply_id=supply_id))

    supply = PaintSupply(id=supply_id)
    form.populate_obj(supply)

    status, message = update_supply(supply)

    if status:
        return redirect(url_for('supplies_get', success=Success.UPDATED_SUPPLY.value))
    else:
        return render_template('supply.html', form=form,
                               action=url_for('edit_supply_post', supply_id=supply_id),
                               error=message)


@app.route('/supplies/new', methods=['GET'])
@login_required
@admin_only
def new_supply_get():
    form = AdminSupplyForm()
    form.paint_id.choices = [('', 'Не обрано')] + \
                            [(str(paint['id']), paint['code'] + ' - ' + paint['name']) for paint in get_paints()]

    return render_template('supply.html', form=form,
                           action=url_for('new_supply_post'))


@app.route('/supplies/new', methods=['POST'])
@login_required
@admin_only
def new_supply_post():
    form = AdminSupplyForm()
    form.paint_id.choices = [('', 'Не обрано')] + \
                            [(str(paint['id']), paint['code'] + ' - ' + paint['name']) for paint in get_paints()]

    if not form.validate_on_submit():
        return render_template('supply.html', form=form,
                               action=url_for('new_supply_post'))

    supply = PaintSupply()
    form.populate_obj(supply)

    status, message = add_supply(supply)

    if status:
        return redirect(url_for('supplies_get', success=Success.ADDED_SUPPLY.value))
    else:
        return render_template('supply.html', form=form,
                               action=url_for('new_supply_post'),
                               error=message)


@app.route('/supplies/delete/<int:supply_id>', methods=['GET'])
@login_required
@admin_only
def delete_supply_get(supply_id):
    status, message = delete_supply(supply_id)

    if status:
        return redirect(url_for('supplies_get', success=Success.DELETED_SUPPLY.value))
    else:
        return redirect(url_for('supplies_get', error=Error.SUPPLY_INTEGRITY.value))
