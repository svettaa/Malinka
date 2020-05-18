from flask import render_template, url_for, redirect, request
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash

from app import app
from app.forms import ChangePasswordForm
from app.api.api_client import *


@app.route('/cabinet/password', methods=['GET'])
@login_required
def change_user_password_get():
    form = ChangePasswordForm()
    return render_template('password.html', form=form,
                           action=url_for('change_user_password_post'),
                           error=(request.args.get('error')),
                           success=(request.args.get('success')))


@app.route('/cabinet/password', methods=['POST'])
@login_required
def change_user_password_post():
    form = ChangePasswordForm()
    client_id = current_user.id

    if not check_password_hash(get_client_password(client_id), form.old_password.data):
        return render_template('password.html', form=form,
                               action=url_for('change_user_password_post'),
                               error='Неправильний старий пароль')

    if not form.validate_on_submit():
        return render_template('password.html', form=form,
                               action=url_for('change_user_password_post'))

    status, message = set_client_password(client_id, form.new_password.data)

    if status:
        return redirect(url_for('edit_user_profile_get', success=message))
    else:
        return render_template('password.html', form=form,
                               action=url_for('change_user_password_post'),
                               error=message)
