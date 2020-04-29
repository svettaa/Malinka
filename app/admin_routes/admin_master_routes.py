from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError, DataError

from app import app
from app.models import *
from app.message_codes import *


@app.route('/masters', methods=['GET'])
def masters_get():
    return render_template('masters.html')


@app.route('/masters/<int:master_id>', methods=['GET'])
def edit_master_get(master_id):
    return render_template('master.html')
