from flask import render_template
from flask_login import login_required

from app import app
from app.login import master_only


@app.route('/cabinet/timetable', methods=['GET'])
@login_required
@master_only
def master_timetable_get():
    return render_template('master_timetable.html')