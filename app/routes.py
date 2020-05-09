from flask import render_template, url_for, redirect, request
from flask_login import logout_user, login_user, login_required, current_user
from datetime import datetime

from app import app, db, login_manager
from app.models import Client
from app.forms import LoginForm
from app.message_codes import *


@login_manager.user_loader
def load_user(user_id):
    return Client.query.get(int(user_id))


@app.context_processor
def pass_default_parameters():
    return {'now': datetime.utcnow(),
            'current_user': current_user}


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login_get'))


@app.route('/')
def index():
    masters = db.engine.execute('SELECT surname, first_name, second_name '
                                'FROM Master INNER JOIN Client ON Master.id = Client.id '
                                'WHERE is_hired = True;').fetchall()

    categories_proxy = db.engine.execute('SELECT id, name '
                                         'FROM Category;').fetchall()

    categories = []
    for category in categories_proxy:
        procedures = db.engine.execute('SELECT name, info, price_min, price_max '
                                       'FROM Procedure '
                                       'WHERE category_id = %s;',
                                       category['id']).fetchall()
        new_item = {'name': category['name'],
                    'procedures': procedures}
        categories.append(new_item)

    return render_template('index.html', categories=categories, masters=masters)


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
