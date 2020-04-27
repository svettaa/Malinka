from flask import render_template

from app import app, db
from app.models import *


@app.route('/')
def index():
    # masters = Master.query.all()
    # categories = Category.query.all()

    masters = db.engine.execute('SELECT surname, first_name, second_name '
                                'FROM Master;').fetchall()

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


@app.route('/categories')
def categories():
    return render_template('categories.html')


@app.route('/categories/<int:category_id>')
def category(category_id):
    return render_template('category.html')
