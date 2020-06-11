from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_uploads import UploadSet, configure_uploads, IMAGES
from datetime import time
from sqlalchemy.engine import create_engine

import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['DEBUG'] = os.environ.get('DEBUG')
app.config['CSRF_ENABLED'] = os.environ.get('CSRF_ENABLED')
app.config['CSRF_SESSION_KEY'] = os.environ.get('CSRF_SESSION_KEY')
app.config['WTF_CSRF_SECRET_KEY'] = os.environ.get('WTF_CSRF_SECRET_KEY')
app.config['WTF_CSRF_TIME_LIMIT'] = int(os.environ.get('WTF_CSRF_TIME_LIMIT'))
app.config['UPLOADED_PHOTOS_DEST'] = os.environ.get('UPLOADED_PHOTOS_DEST')

app.config['WORKING_DAY_START'] = time(9, 0, 0)
app.config['WORKING_DAY_END'] = time(20, 0, 0)

login_manager = LoginManager(app)
db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
migrate = Migrate(app, db)
admin = Admin(app, template_mode='bootstrap3')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, (photos,))

from app.routes import *
from app.socket_io import *
from app.rest_api import *
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
