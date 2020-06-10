from flask import render_template
from flask_login import login_required

from app import app
from app.forms import AdminClientForm


@app.route('/profile', methods=['GET'])
@login_required
def edit_user_profile_get():
    return render_template('user/profile.html', csrf_token=AdminClientForm().csrf_token)
