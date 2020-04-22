from flask_admin.contrib.sqla import ModelView

from app.models import *


class ClientView(ModelView):
    form_excluded_columns = ['photo']


class MasterView(ModelView):
    inline_models = [ScheduleChange]
    form_excluded_columns = ['photo']


class ScheduleChangeView(ModelView):
    pass


class CategoryView(ModelView):
    inline_models = [Procedure]


class ProcedureView(ModelView):
    pass
