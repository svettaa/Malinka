from flask_login import login_required
from flask import jsonify, request

from app import app
from app.login import admin_only
from app.api.api_client import reset_client_password, delete_client_password


@app.route('/reset_password', methods=['GET'])
@login_required
@admin_only
def reset_password():
    try:
        client_id = int(request.args.get('id'))
        status, message = reset_client_password(client_id)
        return jsonify({'status': status,
                        'message': message})
    except ValueError:
        return jsonify({'status': False,
                        'message': 'Некоректний формат номера клієнта'})


@app.route('/delete_password', methods=['GET'])
@login_required
@admin_only
def delete_password():
    try:
        client_id = int(request.args.get('id'))
        status, message = delete_client_password(client_id)
        return jsonify({'status': status,
                        'message': message})
    except ValueError:
        return jsonify({'status': False,
                        'message': 'Некоректний формат номера клієнта'})
