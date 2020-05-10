from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app import app
from app.api.api_client import *


@app.route('/cabinet/favourite_masters/delete/<int:master_id>', methods=['GET'])
@login_required
def delete_favourite_master_get(master_id):
    status, message = delete_client_favourite_master(current_user.id, master_id)

    if status:
        return redirect(url_for('edit_user_profile_get',
                                success=message))
    else:
        return redirect(url_for('edit_user_profile_get',
                                error=message))


@app.route('/cabinet/favourite_procedures/delete/<int:procedure_id>', methods=['GET'])
@login_required
def delete_favourite_procedure_get(procedure_id):
    status, message = delete_client_favourite_procedure(current_user.id, procedure_id)

    if status:
        return redirect(url_for('edit_user_profile_get',
                                success=message))
    else:
        return redirect(url_for('edit_user_profile_get',
                                error=message))
