from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome

app = Flask(__name__)
app.config.from_pyfile('config.py')

login_manager = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin(app, template_mode='bootstrap3')
bootstrap = Bootstrap(app)
font_awesome = FontAwesome(app)

from app.routes import *
from app.admin_routes import *
from app.user_routes import *
from app.master_routes import *
from app.models import *
from app.admin_views import *

admin.add_view(ClientView(Client, db.session))
admin.add_view(MasterView(Master, db.session))
admin.add_view(ScheduleChangeView(ScheduleChange, db.session))
admin.add_view(CategoryView(Category, db.session))
admin.add_view(ProcedureView(Procedure, db.session))
admin.add_view(AppointmentView(Appointment, db.session))
admin.add_view(AppointmentPaintView(AppointmentPaint, db.session))
admin.add_view(PaintView(Paint, db.session))
admin.add_view(PaintSupplyView(PaintSupply, db.session))
admin.add_view(MasterProcedureView(MasterProcedure, db.session))
