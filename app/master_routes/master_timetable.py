from flask import render_template

from app import app


@app.route('/cabinet/timetable', methods=['GET'])
def master_timetable_get():
    return render_template('master_timetable.html')