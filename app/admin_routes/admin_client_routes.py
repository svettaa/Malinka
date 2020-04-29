from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError, DataError

from app import app
from app.models import *
from app.message_codes import *


@app.route('/clients', methods=['GET'])
def clients_get():
    return render_template('clients.html')


@app.route('/clients/<int:client_id>', methods=['GET'])
def edit_client_get(client_id):
    return render_template('client.html')
