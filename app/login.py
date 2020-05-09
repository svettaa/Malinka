import functools

from flask import render_template, url_for, redirect, request
from flask_login import logout_user, login_user, login_required, current_user

from app import app, db, login_manager
from app.models import Client
from app.forms import LoginForm
from app.message_codes import *


@login_manager.user_loader
def load_user(user_id):
    return Client.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login_get'))


def admin_only(function):
    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        if not current_user.is_admin():
            return redirect(url_for('index'))
        else:
            return function(*args, **kwargs)

    return wrapped


def master_only(function):
    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        if not current_user.is_master():
            return redirect(url_for('index'))
        else:
            return function(*args, **kwargs)

    return wrapped


@app.route('/login', methods=['GET'])
def login_get():
    form = LoginForm()
    return render_template('login.html', form=form,
                           error=get_error_message(request.args.get('error')),
                           success=get_success_message(request.args.get('success')))


@app.route('/login', methods=['POST'])
def login_post():
    form = LoginForm()

    if not form.validate_on_submit():
        return render_template('login.html', form=form)

    user = Client.query.filter(Client.phone == form.phone.data).first()

    if not user:
        return render_template('login.html', form=form,
                               error=Error.USER_NOT_EXISTS.value)

    login_user(user)

    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
