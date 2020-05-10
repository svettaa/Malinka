from flask import render_template
from flask_login import current_user
from datetime import datetime

from app import app, db


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
        procedures = db.engine.execute('SELECT name, info, price_min, price_max '
                                       'FROM Procedure '
                                       'WHERE category_id = %s;',
                                       category['id']).fetchall()
        new_item = {'name': category['name'],
                    'procedures': procedures}
        categories.append(new_item)

    return render_template('index.html', categories=categories, masters=masters)
