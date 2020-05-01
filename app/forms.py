from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired


class BaseForm(FlaskForm):
    pass


class AdminCategoryForm(BaseForm):
    name = StringField('Назва категорії', validators=[InputRequired('Введіть назву категорії')])
