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


class AppointmentView(ModelView):
    pass


class AppointmentPaintView(ModelView):
    pass


class PaintView(ModelView):
    inline_models = [PaintSupply]


class PaintSupplyView(ModelView):
    pass


class MasterProcedureView(ModelView):
    pass
