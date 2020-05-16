from flask import render_template
from flask_login import current_user
from datetime import datetime

from app import app, db
from app.api.api_client import get_client_favourite_procedures


@app.context_processor
def pass_default_parameters():
    return {'now': datetime.utcnow(),
            'current_user': current_user}


@app.route('/')
def index():
    masters = db.engine.execute('SELECT surname, first_name, second_name '
                                'FROM Master INNER JOIN Client ON Master.id = Client.id '
                                'WHERE is_hired = True;').fetchall()

    categories_proxy = db.engine.execute('SELECT id, name '
                                         'FROM Category;').fetchall()

    categories = []
    for category in categories_proxy:
        procedures = db.engine.execute('SELECT id, name, info, price_min, price_max '
                                       'FROM Procedure '
                                       'WHERE category_id = %s;',
                                       category['id']).fetchall()
        new_item = {'name': category['name'],
                    'procedures': procedures}
        categories.append(new_item)

    if current_user.is_authenticated:
        favourite_procedures = get_client_favourite_procedures(current_user.id)
    else:
        favourite_procedures = None

    return render_template('index.html',
                           categories=categories,
                           masters=masters,
                           favourite_procedures=favourite_procedures)
