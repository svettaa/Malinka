from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError, DataError

from app import app
from app.models import *
from app.message_codes import *


@app.route('/supplies')
def supplies():
    return render_template('supplies.html')


@app.route('/supplies/<int:supply_id>')
def supply(supply_id):
    return render_template('supply.html')
