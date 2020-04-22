from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin(app, template_mode='bootstrap3')

from app.routes import *
from app.models import *
from app.admin_views import *

admin.add_view(ClientView(Client, db.session))
admin.add_view(MasterView(Master, db.session))
admin.add_view(ScheduleChangeView(ScheduleChange, db.session))
admin.add_view(CategoryView(Category, db.session))
admin.add_view(ProcedureView(Procedure, db.session))
