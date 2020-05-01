from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TextAreaField, RadioField
from wtforms.validators import InputRequired, Optional, NumberRange
from wtforms.fields.html5 import DateField, TelField, EmailField


class BaseForm(FlaskForm):
    pass


class AdminCategoryForm(BaseForm):
    name = StringField('Назва категорії', validators=[InputRequired('Введіть назву категорії')])


class AdminProcedureForm(BaseForm):
    category_id = SelectField('Назва категорії', validators=[InputRequired('Виберіть категорію')],
                              coerce=int)
    name = StringField('Назва процедури', validators=[InputRequired('Введіть назву процедури')])
    price_min = IntegerField('Мінімальна ціна', validators=[InputRequired('Введіть мінімальну ціну'),
                                                            NumberRange(min=0,
                                                                        message='Ціна не може бути від\'ємною')])
    price_max = IntegerField('Максимальна ціна', validators=[Optional(),
                                                             NumberRange(min=0,
                                                                         message='Ціна не може бути від\'ємною')])
    info = TextAreaField('Додаткова інформація', validators=[Optional()])


class AdminPaintForm(BaseForm):
    code = StringField('Номер фарби', validators=[InputRequired('Введіть номер фарби')])
    name = StringField('Назва фарби', validators=[InputRequired('Введіть назву фарби')])


class AdminSupplyForm(BaseForm):
    paint_id = SelectField('Фарба', validators=[InputRequired('Виберіть фарбу')],
                           coerce=int)
    amount = IntegerField('Кількість, мл', validators=[InputRequired('Введіть кількість фарби'),
                                                       NumberRange(min=1, message='Кількість має бути більше нуля')])
    supply_date = DateField('Дата', validators=[InputRequired('Введіть дату')])


class AdminClientForm(BaseForm):
    surname = StringField('Прізвище', validators=[InputRequired('Введіть прізвище')])
    first_name = StringField('Ім\'я', validators=[InputRequired('Введіть ім\'я')])
    second_name = StringField('По-батькові', validators=[Optional()])
    is_male = RadioField('Стать', validators=[InputRequired('Виберіть стать')],
                         choices=[(1, 'Чоловіча'), (0, 'Жіноча')], coerce=int)
    phone = TelField('Телефон', validators=[InputRequired('Введіть телефон')])
    email = EmailField('Email', validators=[Optional()])


class AdminEditMasterForm(BaseForm):
    even_schedule = RadioField('Графік', validators=[InputRequired('Оберіть графік')],
                               choices=[(1, 'Парний'), (0, 'Непарний')], coerce=int)
    is_hired = RadioField('Статус', validators=[InputRequired('Оберіть статус')],
                          choices=[(1, 'Працює'), (0, 'Звільнено')], coerce=int)


class AdminNewMasterForm(AdminEditMasterForm):
    id = SelectField('Користувач', validators=[InputRequired('Виберіть користувача')],
                     coerce=int)
