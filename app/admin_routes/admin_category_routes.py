from flask import render_template
from flask_login import login_required

from app import app
from app.forms import AdminCategoryForm
from app.login import admin_only


@app.route('/categories')
@login_required
@admin_only
def categories_get():
    return render_template('categories.html', csrf_token=AdminCategoryForm().csrf_token)
