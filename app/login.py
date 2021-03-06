import functools

from flask import render_template, url_for, redirect, request, session
from flask_login import logout_user, login_user, login_required, current_user
from werkzeug.security import check_password_hash

from app import app, db, login_manager
from app.models import Client
from app.forms import LoginForm


@login_manager.user_loader
def load_user(user_id):
    return Client.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_callback():
    url = request.path + '?'
    for arg in request.args:
        url = url + arg + '=' + request.args.get(arg) + '&'

    session['next'] = url
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
                           error=(request.args.get('error')),
                           success=(request.args.get('success')))


@app.route('/login', methods=['POST'])
def login_post():
    form = LoginForm()

    if not form.validate_on_submit():
        return render_template('login.html', form=form)

    user = Client.query.filter(Client.phone == form.phone.data).first()

    if not user:
        return render_template('login.html', form=form,
                               error='Не існує користувача з таким номером телефону')

    if user.password is None:
        return render_template('login.html', form=form,
                               error='Адміністратор ще не встановив Вам пароль')

    if not check_password_hash(user.password, form.password.data):
        return render_template('login.html', form=form,
                               error='Неправильний пароль')

    login_user(user)

    if 'next' in session:
        next = session['next']
        del session['next']
        return redirect(next)
    else:
        return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
