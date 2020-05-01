from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, Optional


class BaseForm(FlaskForm):
    pass


class AdminCategoryForm(BaseForm):
    name = StringField('Назва категорії', validators=[InputRequired('Введіть назву категорії')])


class AdminProcedureForm(BaseForm):
    category_id = SelectField('Назва категорії', validators=[InputRequired('Виберіть категорію')],
                              coerce=int)
    name = StringField('Назва процедури', validators=[InputRequired('Введіть назву процедури')])
    price_min = IntegerField('Мінімальна ціна', validators=[InputRequired('Введіть мінімальну ціну')])
    price_max = IntegerField('Максимальна ціна', validators=[Optional()])
    info = TextAreaField('Додаткова інформація', validators=[Optional()])


class AdminPaintForm(BaseForm):
    code = StringField('Номер фарби', validators=[InputRequired('Введіть номер фарби')])
    name = StringField('Назва фарби', validators=[InputRequired('Введіть назву фарби')])
